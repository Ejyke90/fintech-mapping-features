# GitHub Pages Setup Instructions

This document provides the final steps needed to enable GitHub Pages for your repository.

## 📋 Prerequisites

All code has been set up! Now you need to configure GitHub repository settings.

## 🔧 GitHub Repository Configuration

### Step 1: Enable GitHub Pages

1. Go to your repository: `https://github.com/Ejyke90/fintech-mapping-features`
2. Click on **Settings** tab
3. Scroll down to **Pages** (left sidebar under "Code and automation")
4. Under **Source**, select:
   - **Source**: GitHub Actions
   
   ✅ This allows the GitHub Actions workflow to deploy the site

### Step 2: Configure GitHub Actions Permissions

1. In **Settings** → **Actions** → **General**
2. Scroll to **Workflow permissions**
3. Select **Read and write permissions**
4. Check ✅ **Allow GitHub Actions to create and approve pull requests**
5. Click **Save**

### Step 3: Trigger Initial Deployment

#### Option A: Push to Main Branch
```bash
git add .
git commit -m "feat: Add Docusaurus documentation site with GitHub Pages deployment"
git push origin main
```

#### Option B: Manual Workflow Trigger
1. Go to **Actions** tab
2. Click **Deploy Documentation to GitHub Pages**
3. Click **Run workflow** → **Run workflow**

### Step 4: Monitor Deployment

1. Go to **Actions** tab
2. Watch the workflow run (takes ~3-5 minutes)
3. Once complete, site will be available at:
   
   **🌐 https://ejyke90.github.io/fintech-mapping-features/**

## 🎉 What You'll See

Your documentation site will include:

### 📘 Main Pages
- **Home**: Overview of the monorepo
- **Architecture**: System design and component diagram
- **Getting Started**: Setup and installation guide
- **XML Sanitizer**: Module documentation
- **Intelligent Mapping Generator**: Module documentation

### 🔌 API Documentation
- Interactive Swagger-style API documentation
- Auto-generated from Spring Boot OpenAPI specs
- Try-it-out functionality

### 🎨 Features
- Dark mode toggle
- Search functionality (Algolia - optional)
- Mobile responsive
- Fast static site generation

## 🔄 Updating Documentation

### For Content Changes

1. Edit Markdown files in `docs/docs/`
2. Commit and push to `main`
3. GitHub Actions automatically rebuilds and deploys

### For API Changes

API documentation updates automatically when:
1. You update Spring Boot `@RestController` annotations
2. Push to `main` branch
3. GitHub Actions:
   - Builds Spring Boot apps
   - Starts services
   - Downloads OpenAPI specs
   - Generates API docs
   - Deploys to GitHub Pages

## 🧪 Testing Locally

Before pushing, test locally:

```bash
# Terminal 1: Start Docusaurus
cd docs
npm start
# Visit http://localhost:3000/fintech-mapping-features/

# Terminal 2 (optional): Generate API docs from running services
cd ..
./gradlew :xml-sanitizer:bootRun &
./gradlew :intelligent-mapping-generator:bootRun &
sleep 30

mkdir -p openapi-specs
curl http://localhost:8080/v3/api-docs -o openapi-specs/xml-sanitizer-openapi.json
curl http://localhost:8081/v3/api-docs -o openapi-specs/mapping-generator-openapi.json

cd docs
npm run gen-api-docs
```

## 📝 Quick Reference

| Task | Command |
|------|---------|
| Start local dev server | `cd docs && npm start` |
| Build for production | `cd docs && npm run build` |
| Generate API docs | `cd docs && npm run gen-api-docs` |
| Clean cache | `cd docs && npm run clear` |

## 🐛 Troubleshooting

### Workflow Fails
- Check **Actions** tab for detailed logs
- Common issues:
  - Services not starting (increase sleep time in workflow)
  - OpenAPI endpoints not accessible
  - Node.js memory issues (increase `NODE_OPTIONS`)

### Site Not Accessible
- Ensure GitHub Pages is enabled (Settings → Pages)
- Check workflow completed successfully
- Wait 1-2 minutes for DNS propagation
- Try hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

### API Docs Not Showing
- Verify OpenAPI specs downloaded correctly (check workflow logs)
- Ensure `springdoc` dependencies are in `build.gradle`
- Check `application.properties` has correct configuration

## 🚀 Next Steps

After deployment:

1. ✅ Visit your site: https://ejyke90.github.io/fintech-mapping-features/
2. ✅ Test all navigation links
3. ✅ Verify API documentation is accessible
4. ✅ Share the URL with your team
5. ✅ Add the URL to your repository description
6. ✅ Add a badge to your main README (optional):

```markdown
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://ejyke90.github.io/fintech-mapping-features/)
```

## 📞 Need Help?

If you encounter issues:
1. Check workflow logs in **Actions** tab
2. Review this document
3. Open an issue in the repository

## 🎊 Congratulations!

You now have a professional, automatically-updated documentation site for your fintech monorepo! 🎉
