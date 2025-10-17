# Multi-Branch GitHub Pages Deployment Strategy

> **Goal**: Deploy different versions of documentation from different git branches to separate URLs.

---

## 🎯 Use Cases

- **Feature branches**: Preview docs for feature branches before merging
- **Version branches**: Maintain docs for multiple product versions (v1.x, v2.x, v3.x)
- **Environment branches**: Different docs for dev, staging, production
- **A/B Testing**: Test different documentation approaches

---

## 🏗️ Architecture Options

### Option 1: Subdirectories by Branch (Recommended)
Each branch deploys to a subdirectory:
```
https://ejyke90.github.io/fintech-mapping-features/           → main branch
https://ejyke90.github.io/fintech-mapping-features/dev/       → dev branch
https://ejyke90.github.io/fintech-mapping-features/feature-x/ → feature-x branch
https://ejyke90.github.io/fintech-mapping-features/v1.0/      → v1.0 branch
```

### Option 2: Docusaurus Versioning (Built-in)
Use Docusaurus native versioning:
```
https://ejyke90.github.io/fintech-mapping-features/           → Latest
https://ejyke90.github.io/fintech-mapping-features/docs/1.0.0/
https://ejyke90.github.io/fintech-mapping-features/docs/2.0.0/
```

### Option 3: Multiple GitHub Pages Sites
Deploy to completely different repositories/URLs:
```
https://ejyke90.github.io/fintech-mapping-features-main/
https://ejyke90.github.io/fintech-mapping-features-dev/
https://ejyke90.github.io/fintech-mapping-features-v1/
```

### Option 4: Custom Domain with Subdomains
Use custom domains:
```
https://docs.yourcompany.com/           → main
https://dev.docs.yourcompany.com/       → dev
https://v1.docs.yourcompany.com/        → v1.0
```

---

## 🚀 Implementation Guide

## Strategy 1: Branch-Based Subdirectories (RECOMMENDED)

### Step 1: Update GitHub Actions Workflow

Replace `.github/workflows/deploy-docs.yml` with this:

```yaml
name: Deploy Docusaurus to GitHub Pages (Multi-Branch)

on:
  push:
    branches:
      - main
      - dev
      - staging
      - 'release/**'    # Match release/v1.0, release/v2.0, etc.
      - 'feature/**'    # Match all feature branches
  workflow_dispatch:
    inputs:
      branch:
        description: 'Branch to deploy'
        required: true
        default: 'main'

permissions:
  contents: write  # Changed to write for gh-pages branch
  pages: write
  id-token: write

concurrency:
  group: "pages-${{ github.ref_name }}"  # Allow parallel deploys per branch
  cancel-in-progress: false

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Determine deployment path
        id: deploy-path
        run: |
          BRANCH_NAME="${{ github.ref_name }}"
          
          # Sanitize branch name for URL
          # Replace / with - and remove special characters
          DEPLOY_PATH=$(echo "$BRANCH_NAME" | sed 's/\//-/g' | sed 's/[^a-zA-Z0-9-]/-/g' | tr '[:upper:]' '[:lower:]')
          
          # Main branch goes to root
          if [ "$BRANCH_NAME" == "main" ]; then
            DEPLOY_PATH=""
            BASE_URL="/fintech-mapping-features/"
          else
            BASE_URL="/fintech-mapping-features/${DEPLOY_PATH}/"
          fi
          
          echo "deploy_path=$DEPLOY_PATH" >> $GITHUB_OUTPUT
          echo "base_url=$BASE_URL" >> $GITHUB_OUTPUT
          echo "branch_name=$BRANCH_NAME" >> $GITHUB_OUTPUT
          
          echo "📍 Deploying branch '$BRANCH_NAME' to: $BASE_URL"
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: docs/package-lock.json
      
      - name: Setup Java (if needed)
        uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: 'gradle'
      
      - name: Build Services
        run: |
          ./gradlew :intelligent-mapping-generator:build -x test
      
      - name: Start Service & Extract OpenAPI Spec
        run: |
          ./gradlew :intelligent-mapping-generator:bootRun &
          SERVICE_PID=$!
          
          # Wait for service
          timeout=60
          count=0
          while [ $count -lt $timeout ]; do
            if curl -f http://localhost:8081/actuator/health > /dev/null 2>&1; then
              echo "✅ Service is ready"
              break
            fi
            sleep 1
            count=$((count + 1))
          done
          
          # Download OpenAPI spec
          mkdir -p openapi-specs
          curl -f http://localhost:8081/v3/api-docs -o openapi-specs/intelligent-mapping-generator-openapi.json || \
            echo '{"openapi":"3.0.1","info":{"title":"Intelligent Mapping Generator API","version":"0.0.1"}}' > openapi-specs/intelligent-mapping-generator-openapi.json
          
          # Placeholder for xml-sanitizer
          echo '{"openapi":"3.0.1","info":{"title":"XML Sanitizer API (Coming Soon)","version":"0.0.1"}}' > openapi-specs/xml-sanitizer-openapi.json
          
          kill $SERVICE_PID || true
      
      - name: Install Documentation Dependencies
        working-directory: ./docs
        run: npm ci
      
      - name: Update Docusaurus Config for Branch
        working-directory: ./docs
        run: |
          # Create a branch-specific config
          cat > docusaurus.config.branch.js << 'EOF'
          module.exports = {
            baseUrl: process.env.BASE_URL || '/fintech-mapping-features/',
            url: 'https://ejyke90.github.io',
            // Add branch banner for non-main branches
            themeConfig: {
              announcementBar: process.env.BRANCH_NAME !== 'main' ? {
                id: 'branch_version',
                content: `📋 You are viewing documentation for branch: <strong>${process.env.BRANCH_NAME}</strong>. <a href="/fintech-mapping-features/">View latest (main)</a>`,
                backgroundColor: '#ffd700',
                textColor: '#000',
                isCloseable: false,
              } : undefined,
            },
          };
          EOF
      
      - name: Build Docusaurus
        working-directory: ./docs
        env:
          BASE_URL: ${{ steps.deploy-path.outputs.base_url }}
          BRANCH_NAME: ${{ steps.deploy-path.outputs.branch_name }}
        run: |
          # Merge branch config with main config
          npm run build
      
      - name: Add Branch Index (for non-main branches)
        if: github.ref_name != 'main'
        working-directory: ./docs/build
        run: |
          # Create a .nojekyll file to preserve _next directories
          touch .nojekyll
          
          # Add metadata file
          cat > branch-info.json << EOF
          {
            "branch": "${{ steps.deploy-path.outputs.branch_name }}",
            "commit": "${{ github.sha }}",
            "deployed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
            "deployed_by": "${{ github.actor }}"
          }
          EOF
      
      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/build
          destination_dir: ${{ steps.deploy-path.outputs.deploy_path }}
          keep_files: true  # Keep other branch deployments
          commit_message: |
            Deploy docs from branch: ${{ steps.deploy-path.outputs.branch_name }}
            Commit: ${{ github.sha }}
      
      - name: Add deployment comment to PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const deployPath = '${{ steps.deploy-path.outputs.deploy_path }}';
            const baseUrl = deployPath 
              ? `https://ejyke90.github.io/fintech-mapping-features/${deployPath}/`
              : 'https://ejyke90.github.io/fintech-mapping-features/';
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## 📚 Documentation Preview\n\n✅ Documentation deployed successfully!\n\n🔗 **Preview URL**: ${baseUrl}\n\n_This preview will be updated with every push to this branch._`
            });
      
      - name: Create deployment summary
        run: |
          echo "## 🚀 Deployment Summary" >> $GITHUB_STEP_SUMMARY
          echo "" >> $GITHUB_STEP_SUMMARY
          echo "- **Branch**: \`${{ steps.deploy-path.outputs.branch_name }}\`" >> $GITHUB_STEP_SUMMARY
          echo "- **Commit**: \`${{ github.sha }}\`" >> $GITHUB_STEP_SUMMARY
          echo "- **URL**: [${{ steps.deploy-path.outputs.base_url }}](https://ejyke90.github.io${{ steps.deploy-path.outputs.base_url }})" >> $GITHUB_STEP_SUMMARY
          echo "- **Deployed**: $(date -u +%Y-%m-%d\ %H:%M:%S\ UTC)" >> $GITHUB_STEP_SUMMARY

  # Optional: Cleanup old branch deployments
  cleanup:
    runs-on: ubuntu-latest
    if: github.event_name == 'delete' || (github.event_name == 'pull_request' && github.event.action == 'closed')
    
    steps:
      - name: Checkout gh-pages branch
        uses: actions/checkout@v4
        with:
          ref: gh-pages
      
      - name: Remove branch deployment
        run: |
          BRANCH_NAME="${{ github.event.ref }}"
          DEPLOY_PATH=$(echo "$BRANCH_NAME" | sed 's/\//-/g' | sed 's/[^a-zA-Z0-9-]/-/g' | tr '[:upper:]' '[:lower:]')
          
          if [ -d "$DEPLOY_PATH" ]; then
            git rm -rf "$DEPLOY_PATH"
            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git commit -m "Remove deployment for deleted branch: $BRANCH_NAME"
            git push
            echo "✅ Removed deployment for branch: $BRANCH_NAME"
          else
            echo "ℹ️ No deployment found for branch: $BRANCH_NAME"
          fi
```

### Step 2: Update Docusaurus Config

Update `docs/docusaurus.config.ts` to support dynamic baseUrl:

```typescript
import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// Get baseUrl from environment or default
const baseUrl = process.env.BASE_URL || '/fintech-mapping-features/';
const branchName = process.env.BRANCH_NAME || 'main';
const isMainBranch = branchName === 'main';

const config: Config = {
  title: 'Fintech Mapping Features',
  tagline: 'Multi-module Spring Boot Microservices for Fintech Data Transformation',
  favicon: 'img/favicon.ico',

  url: 'https://ejyke90.github.io',
  baseUrl: baseUrl,
  
  organizationName: 'Ejyke90',
  projectName: 'fintech-mapping-features',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/Ejyke90/fintech-mapping-features/tree/main/docs/',
        },
        blog: {
          showReadingTime: true,
          editUrl: 'https://github.com/Ejyke90/fintech-mapping-features/tree/main/docs/',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Show branch banner for non-main branches
    ...(!isMainBranch && {
      announcementBar: {
        id: 'branch_version',
        content: `📋 You are viewing documentation for branch: <strong>${branchName}</strong>. <a href="/fintech-mapping-features/">View latest (main)</a>`,
        backgroundColor: '#ffd700',
        textColor: '#000',
        isCloseable: false,
      },
    }),
    
    navbar: {
      title: 'Fintech Mapping Features',
      logo: {
        alt: 'Fintech Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Documentation',
        },
        {to: '/blog', label: 'Blog', position: 'left'},
        // Show branch dropdown for multi-branch deployments
        ...(!isMainBranch ? [{
          type: 'dropdown',
          label: `Branch: ${branchName}`,
          position: 'right',
          items: [
            {
              label: 'main (latest)',
              href: 'https://ejyke90.github.io/fintech-mapping-features/',
            },
            {
              label: 'dev',
              href: 'https://ejyke90.github.io/fintech-mapping-features/dev/',
            },
            // Add more branches as needed
          ],
        }] : []),
        {
          href: 'https://github.com/Ejyke90/fintech-mapping-features',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Introduction',
              to: '/docs/',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/Ejyke90/fintech-mapping-features',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Fintech Mapping Features. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
```

### Step 3: Create Branch Index Page (Optional)

Create `docs/static/branches.html` to list all deployed branches:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation Branches - Fintech Mapping Features</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: #f5f5f5;
        }
        h1 { color: #333; }
        .branch-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }
        .branch-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .branch-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .branch-name {
            font-size: 1.25rem;
            font-weight: bold;
            color: #0066cc;
            margin-bottom: 0.5rem;
        }
        .branch-link {
            display: inline-block;
            margin-top: 1rem;
            padding: 0.5rem 1rem;
            background: #0066cc;
            color: white;
            text-decoration: none;
            border-radius: 4px;
        }
        .branch-link:hover {
            background: #0052a3;
        }
        .main-branch {
            border: 2px solid #28a745;
        }
    </style>
</head>
<body>
    <h1>📚 Documentation Versions</h1>
    <p>Select a branch to view its documentation:</p>
    
    <div class="branch-list" id="branchList">
        <!-- Branches will be loaded dynamically -->
    </div>

    <script>
        // This would ideally fetch from an API or be generated by CI
        const branches = [
            { name: 'main', url: '/fintech-mapping-features/', description: 'Latest stable version', isMain: true },
            { name: 'dev', url: '/fintech-mapping-features/dev/', description: 'Development version' },
            { name: 'feature-x', url: '/fintech-mapping-features/feature-x/', description: 'Feature X preview' },
        ];

        const branchList = document.getElementById('branchList');
        branches.forEach(branch => {
            const card = document.createElement('div');
            card.className = `branch-card ${branch.isMain ? 'main-branch' : ''}`;
            card.innerHTML = `
                <div class="branch-name">${branch.name}${branch.isMain ? ' 🌟' : ''}</div>
                <p>${branch.description}</p>
                <a href="${branch.url}" class="branch-link">View Documentation →</a>
            `;
            branchList.appendChild(card);
        });
    </script>
</body>
</html>
```

---

## Strategy 2: Docusaurus Native Versioning

For version-based documentation (not branch-based):

### Step 1: Create Version

```bash
cd docs
npm run docusaurus docs:version 1.0.0
```

This creates:
- `versioned_docs/version-1.0.0/` - Copy of current docs
- `versioned_sidebars/version-1.0.0-sidebars.json` - Sidebar config
- `versions.json` - List of versions

### Step 2: Update Workflow

```yaml
- name: Build Docusaurus with Versions
  working-directory: ./docs
  run: npm run build
  # Docusaurus automatically includes all versions
```

### Step 3: Configure Version Dropdown

In `docusaurus.config.ts`:

```typescript
themeConfig: {
  navbar: {
    items: [
      {
        type: 'docsVersionDropdown',
        position: 'right',
      },
    ],
  },
},
```

---

## 📊 Comparison Matrix

| Feature | Branch Subdirs | Docusaurus Versions | Multiple Repos | Custom Subdomains |
|---------|---------------|---------------------|----------------|-------------------|
| **Ease of Setup** | Medium | Easy | Hard | Hard |
| **Cost** | Free | Free | Free | Domain cost |
| **Preview PRs** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Automatic Cleanup** | ✅ Yes | Manual | Manual | Manual |
| **SEO** | Good | Excellent | Good | Excellent |
| **Maintenance** | Low | Low | High | Medium |
| **Best For** | Feature previews | Version docs | Separate projects | Enterprise |

---

## 🧹 Cleanup Old Deployments

### Automatic Cleanup Script

Create `.github/workflows/cleanup-branches.yml`:

```yaml
name: Cleanup Old Branch Deployments

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout gh-pages
        uses: actions/checkout@v4
        with:
          ref: gh-pages
      
      - name: Remove stale branch deployments
        run: |
          # Get list of active branches
          git fetch origin
          ACTIVE_BRANCHES=$(git branch -r | grep -v HEAD | sed 's/origin\///' | sed 's/\//-/g')
          
          # Find deployed directories
          for dir in */; do
            dir_name="${dir%/}"
            if [ "$dir_name" != "main" ] && ! echo "$ACTIVE_BRANCHES" | grep -q "$dir_name"; then
              echo "Removing stale deployment: $dir_name"
              git rm -rf "$dir_name"
            fi
          done
          
          if git diff --staged --quiet; then
            echo "No stale deployments to remove"
          else
            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git commit -m "Cleanup stale branch deployments"
            git push
          fi
```

---

## 🔍 Monitoring & Discovery

### List All Deployed Branches

Add to your main page or create a branches page:

```javascript
// docs/src/pages/branches.tsx
import React, { useEffect, useState } from 'react';
import Layout from '@theme/Layout';

export default function Branches() {
  const [branches, setBranches] = useState([]);

  useEffect(() => {
    fetch('/fintech-mapping-features/branch-list.json')
      .then(res => res.json())
      .then(data => setBranches(data));
  }, []);

  return (
    <Layout title="Documentation Branches">
      <div style={{padding: '2rem'}}>
        <h1>Available Documentation Branches</h1>
        <ul>
          {branches.map(branch => (
            <li key={branch.name}>
              <a href={branch.url}>{branch.name}</a> - {branch.description}
            </li>
          ))}
        </ul>
      </div>
    </Layout>
  );
}
```

---

## 🎯 Recommended Setup for Your Project

Based on your fintech-mapping-features project, I recommend:

1. **Use Strategy 1 (Branch Subdirectories)** for:
   - Feature branch previews
   - Development branch
   
2. **Use Strategy 2 (Docusaurus Versions)** for:
   - Released versions (v1.0, v2.0, etc.)
   - When you want to maintain historical documentation

3. **Workflow**:
   ```
   feature/* → Preview at /fintech-mapping-features/feature-name/
   dev → Preview at /fintech-mapping-features/dev/
   main → Deploy to /fintech-mapping-features/
   tags (v1.0.0) → Create Docusaurus version
   ```

---

## 📝 Summary

✅ **Yes, you can have different GitHub Pages per branch!**

**Best approach**: Use branch-based subdirectories with the workflow I provided above.

**Benefits**:
- ✅ Automatic deployment per branch
- ✅ Preview URLs for PRs
- ✅ Automatic cleanup when branches are deleted
- ✅ No additional cost
- ✅ Easy to maintain

**Next Steps**:
1. Replace your current workflow with the multi-branch version
2. Push changes to different branches
3. Each branch gets its own URL automatically!

Would you like me to implement this for your project now?
