# Enterprise GitHub Actions Setup Guide for Docusaurus + GitHub Pages

> **Audience**: Enterprise teams using GitHub Enterprise with custom runners, security policies, and compliance requirements.

---

## 🏢 Enterprise-Specific Considerations

### 1. GitHub Enterprise Server vs GitHub Enterprise Cloud

**GitHub Enterprise Cloud**: Follows standard GitHub Pages setup  
**GitHub Enterprise Server**: May require additional configuration

---

## 🔐 Security & Compliance Requirements

### Step 1: Verify GitHub Pages is Enabled

In Enterprise settings, GitHub Pages must be enabled:

```bash
# Check with your GitHub Enterprise admin if:
- GitHub Pages is enabled for your organization
- Public pages are allowed (or private if using GHEC)
- Custom domains are permitted
- GitHub Actions is enabled and configured
```

### Step 2: Configure Organization-Level Settings

1. Navigate to: `https://github.com/organizations/YOUR_ORG/settings/actions`
2. Verify the following permissions:
   - ✅ **Actions permissions**: "Allow all actions and reusable workflows" OR specific allowed actions
   - ✅ **Workflow permissions**: "Read and write permissions"
   - ✅ **Allow GitHub Actions to create and approve pull requests**: Enabled

### Step 3: Repository-Level Permissions

1. Navigate to: `https://github.com/YOUR_ORG/YOUR_REPO/settings/actions`
2. Set **Workflow permissions**:
   ```
   ○ Read repository contents and packages permissions
   ● Read and write permissions  ← Select this
   
   ☑ Allow GitHub Actions to create and approve pull requests
   ```

---

## 🔒 Enterprise GitHub Actions Workflow Template

### Complete Workflow with Enterprise Features

Create `.github/workflows/deploy-docs-enterprise.yml`:

```yaml
name: Deploy Docusaurus to GitHub Pages (Enterprise)

on:
  push:
    branches: [main]
  workflow_dispatch:  # Allow manual triggering

# Set required permissions for GitHub Pages deployment
permissions:
  contents: read
  pages: write
  id-token: write

# Allow one concurrent deployment
concurrency:
  group: "pages"
  cancel-in-progress: true

env:
  NODE_VERSION: '20.x'
  JAVA_VERSION: '21'  # If building Java/Spring Boot services
  # Enterprise-specific: Custom registry if using private npm packages
  NPM_REGISTRY: 'https://npm.pkg.github.com'
  
jobs:
  # Job 1: Build Application Services (if applicable)
  build-services:
    name: Build Application Services
    runs-on: [self-hosted, enterprise-runner]  # Use self-hosted runners if required
    # Alternative for GitHub-hosted runners:
    # runs-on: ubuntu-latest
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for git info
      
      # Enterprise: Authenticate to private registries if needed
      - name: Configure Enterprise Maven/Gradle Registry
        if: hashFiles('**/build.gradle', '**/pom.xml')
        run: |
          echo "Configure your enterprise artifact registry here"
          # Example for Maven:
          # mkdir -p ~/.m2
          # echo "${{ secrets.MAVEN_SETTINGS }}" > ~/.m2/settings.xml
        
      - name: Set up Java (if needed)
        if: hashFiles('**/build.gradle', '**/pom.xml')
        uses: actions/setup-java@v4
        with:
          java-version: ${{ env.JAVA_VERSION }}
          distribution: 'temurin'
          cache: 'gradle'  # or 'maven'
      
      - name: Build Services
        if: hashFiles('**/build.gradle', '**/pom.xml')
        run: |
          # Adjust for your build system
          ./gradlew clean build -x test
          # or: mvn clean install -DskipTests
      
      - name: Start Services & Extract API Specs
        if: hashFiles('**/build.gradle', '**/pom.xml')
        run: |
          # Start your services in background
          ./gradlew :your-service:bootRun &
          SERVICE_PID=$!
          
          # Wait for service to be ready
          timeout=60
          count=0
          while [ $count -lt $timeout ]; do
            if curl -f http://localhost:8080/actuator/health > /dev/null 2>&1; then
              echo "Service is ready"
              break
            fi
            sleep 1
            count=$((count + 1))
          done
          
          # Download OpenAPI spec
          mkdir -p openapi-specs
          curl -f http://localhost:8080/v3/api-docs -o openapi-specs/api-spec.json || \
            echo '{"openapi":"3.0.1","info":{"title":"API","version":"1.0.0"}}' > openapi-specs/api-spec.json
          
          # Stop service
          kill $SERVICE_PID || true
      
      - name: Upload API Specs
        uses: actions/upload-artifact@v4
        with:
          name: openapi-specs
          path: openapi-specs/
          retention-days: 1

  # Job 2: Build Documentation
  build-docs:
    name: Build Documentation Site
    needs: build-services  # Wait for services if applicable
    runs-on: [self-hosted, enterprise-runner]  # Use self-hosted runners if required
    # Alternative: runs-on: ubuntu-latest
    
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          cache-dependency-path: docs/package-lock.json
          # Enterprise: Configure custom registry
          registry-url: ${{ env.NPM_REGISTRY }}
      
      # Enterprise: Authenticate to private npm registry
      - name: Authenticate to Enterprise NPM Registry
        if: env.NPM_REGISTRY != 'https://registry.npmjs.org'
        run: |
          echo "//npm.pkg.github.com/:_authToken=${{ secrets.NPM_TOKEN }}" > ~/.npmrc
          echo "@yourorg:registry=https://npm.pkg.github.com" >> ~/.npmrc
      
      - name: Download API Specs
        if: needs.build-services.result == 'success'
        uses: actions/download-artifact@v4
        with:
          name: openapi-specs
          path: openapi-specs/
      
      - name: Install Dependencies
        working-directory: ./docs
        run: npm ci  # Use ci for reproducible builds in CI/CD
      
      - name: Build Docusaurus Site
        working-directory: ./docs
        run: npm run build
        env:
          NODE_OPTIONS: "--max-old-space-size=4096"  # Increase memory if needed
      
      - name: Upload Build Artifact
        uses: actions/upload-artifact@v4
        with:
          name: docusaurus-build
          path: docs/build/
          retention-days: 1

  # Job 3: Deploy to GitHub Pages
  deploy:
    name: Deploy to GitHub Pages
    needs: build-docs
    runs-on: ubuntu-latest  # Can use GitHub-hosted for deployment
    
    # Enterprise: Require approval for production deployments
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    
    steps:
      - name: Download Build Artifact
        uses: actions/download-artifact@v4
        with:
          name: docusaurus-build
          path: build/
      
      - name: Setup Pages
        uses: actions/configure-pages@v4
      
      - name: Upload Pages Artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: build/
      
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

  # Optional: Notify on completion
  notify:
    name: Send Notifications
    needs: [deploy]
    if: always()
    runs-on: ubuntu-latest
    
    steps:
      - name: Send Slack Notification
        if: needs.deploy.result == 'success'
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK_URL }}
          payload: |
            {
              "text": "✅ Documentation deployed successfully to ${{ needs.deploy.outputs.page_url }}"
            }
      
      - name: Send Email Notification
        if: needs.deploy.result == 'failure'
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.MAIL_USERNAME }}
          password: ${{ secrets.MAIL_PASSWORD }}
          subject: "❌ Documentation Deployment Failed"
          to: devops-team@company.com
          from: github-actions@company.com
          body: "Documentation deployment failed. Check workflow run: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
```

---

## 🔑 Required Secrets (Enterprise)

Add these secrets in your repository or organization settings:

| Secret Name | Description | Where to Add |
|------------|-------------|--------------|
| `GITHUB_TOKEN` | Auto-provided | N/A (automatic) |
| `NPM_TOKEN` | Private npm registry auth | Repository/Org secrets |
| `MAVEN_SETTINGS` | Maven settings.xml | Repository secrets |
| `SLACK_WEBHOOK_URL` | Slack notifications | Repository secrets |
| `MAIL_USERNAME` | Email notifications | Repository secrets |
| `MAIL_PASSWORD` | Email auth | Repository secrets |

### Adding Secrets

```bash
# Using GitHub CLI
gh secret set NPM_TOKEN --body "your-token-here"
gh secret set SLACK_WEBHOOK_URL --body "https://hooks.slack.com/..."

# Or via UI:
# Repository → Settings → Secrets and variables → Actions → New repository secret
```

---

## 🏃 Self-Hosted Runners Setup

### Why Use Self-Hosted Runners?

- Private network access required
- Custom tools/dependencies
- Compliance requirements
- Cost optimization for large builds

### Runner Configuration

```yaml
# In your workflow file, specify runner labels:
runs-on: [self-hosted, linux, x64, enterprise]

# Or organization-level runners:
runs-on: [self-hosted, org-runner]
```

### Setting Up Self-Hosted Runner

```bash
# On your enterprise server/VM:
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Configure (get token from Settings → Actions → Runners)
./config.sh --url https://github.com/YOUR_ORG/YOUR_REPO --token YOUR_TOKEN

# Run as service
sudo ./svc.sh install
sudo ./svc.sh start
```

---

## 🛡️ Security Best Practices

### 1. Workflow Security

```yaml
# Restrict permissions to minimum required
permissions:
  contents: read      # Read code
  pages: write        # Deploy pages
  id-token: write     # OIDC token for deployment
  
# Don't use:
# permissions: write-all  ❌ Too permissive
```

### 2. Secrets Management

```yaml
# ✅ Good: Use secrets for sensitive data
- run: npm install
  env:
    NPM_TOKEN: ${{ secrets.NPM_TOKEN }}

# ❌ Bad: Hardcoding secrets
- run: npm install --registry https://user:password@npm.company.com
```

### 3. Dependency Pinning

```yaml
# ✅ Good: Pin action versions
uses: actions/checkout@v4.1.1

# ❌ Bad: Using latest
uses: actions/checkout@latest
```

### 4. Branch Protection

Enable branch protection rules:
- ✅ Require pull request reviews
- ✅ Require status checks to pass
- ✅ Require signed commits
- ✅ Restrict who can push to branches

---

## 📊 Monitoring & Logging

### Enable Workflow Logging

```yaml
- name: Debug Information
  run: |
    echo "Runner: $(hostname)"
    echo "Branch: ${{ github.ref }}"
    echo "Commit: ${{ github.sha }}"
    echo "Actor: ${{ github.actor }}"
    
- name: Enable Debug Logging
  run: npm run build
  env:
    ACTIONS_STEP_DEBUG: true  # Verbose logging
```

### Integrate with Enterprise Monitoring

```yaml
- name: Send Metrics to DataDog
  uses: masci/datadog@v1
  with:
    api-key: ${{ secrets.DATADOG_API_KEY }}
    metrics: |
      deployment.time:${{ steps.deploy.outputs.time }}
      deployment.success:1
```

---

## 🔄 Rollback Strategy

### Strategy 1: Keep Previous Versions

```yaml
- name: Backup Previous Version
  run: |
    if [ -d "docs/build-backup" ]; then
      rm -rf docs/build-backup
    fi
    cp -r docs/build docs/build-backup

- name: Deploy with Rollback Support
  id: deploy
  uses: actions/deploy-pages@v4
  continue-on-error: true

- name: Rollback on Failure
  if: steps.deploy.outcome == 'failure'
  run: |
    echo "Deployment failed, rolling back..."
    mv docs/build-backup docs/build
```

### Strategy 2: Version Tagging

```yaml
- name: Tag Deployment
  run: |
    git tag "docs-v${{ github.run_number }}"
    git push origin "docs-v${{ github.run_number }}"
```

---

## 🧪 Testing Before Deployment

### Add Pre-Deployment Tests

```yaml
  test-docs:
    name: Test Documentation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      
      - name: Install Dependencies
        working-directory: ./docs
        run: npm ci
      
      - name: Lint Documentation
        working-directory: ./docs
        run: npm run lint || true
      
      - name: Check for Broken Links
        working-directory: ./docs
        run: npm run build  # This will fail on broken links
      
      - name: Run Lighthouse CI
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: |
            http://localhost:3000
          uploadArtifacts: true
```

---

## 📋 Enterprise Compliance Checklist

- [ ] GitHub Pages enabled for organization
- [ ] Repository permissions configured
- [ ] Required approvals for production deployments
- [ ] Secrets properly stored and rotated
- [ ] Self-hosted runners configured (if required)
- [ ] Branch protection rules enabled
- [ ] Audit logging enabled
- [ ] Compliance scanning integrated (Snyk, Dependabot)
- [ ] Access control lists (ACLs) configured
- [ ] Custom domain configured (if required)
- [ ] SSL/TLS certificates validated
- [ ] Network policies reviewed
- [ ] Backup and disaster recovery plan in place

---

## 🆘 Troubleshooting Enterprise Issues

### Issue: "Resource not accessible by integration"
**Solution**: Check repository/workflow permissions, ensure `pages: write` permission is set

### Issue: Self-hosted runner not picking up jobs
**Solution**: 
```bash
# Check runner status
cd actions-runner
./svc.sh status

# Check runner logs
sudo journalctl -u actions.runner.* -f
```

### Issue: Private packages not installing
**Solution**: Configure `.npmrc` or Maven settings with proper authentication

### Issue: Deployment succeeds but site not updating
**Solution**: 
1. Clear GitHub Pages cache
2. Check if CNAME file is interfering
3. Verify baseUrl in docusaurus.config.ts

---

## 📞 Support Contacts

- **GitHub Enterprise Admin**: admin@company.com
- **DevOps Team**: devops@company.com
- **Security Team**: security@company.com
- **GitHub Support**: https://support.github.com/

---

**Document Version**: 1.0  
**Last Updated**: October 2025  
**Maintained By**: DevOps Team
