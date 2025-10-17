# AI Prompt Template: Docusaurus + GitHub Pages Setup

> **Purpose**: Use this template to instruct an AI assistant to set up Docusaurus documentation with automated GitHub Pages deployment for your project.

---

## 📋 Prerequisites Checklist

Before using this prompt, gather the following information:

- [ ] GitHub username/organization: `__YOUR_GITHUB_USERNAME__`
- [ ] Repository name: `__YOUR_REPO_NAME__`
- [ ] Default branch name: `__YOUR_BRANCH_NAME__` (usually `main` or `master`)
- [ ] Project name/title: `__YOUR_PROJECT_TITLE__`
- [ ] Project tagline/description: `__YOUR_PROJECT_TAGLINE__`
- [ ] Your full name: `__YOUR_FULL_NAME__`
- [ ] Your job title: `__YOUR_JOB_TITLE__`
- [ ] Your profile image path (optional): `__PATH_TO_YOUR_IMAGE__`
- [ ] Current workspace path: `__YOUR_WORKSPACE_PATH__`

---

## 🤖 AI Prompt Template

Copy and paste the following prompt to your AI assistant (after replacing placeholders):

```
I need you to set up Docusaurus documentation with automated GitHub Pages deployment for my project.

## Project Information
- **GitHub Username/Org**: __YOUR_GITHUB_USERNAME__
- **Repository Name**: __YOUR_REPO_NAME__
- **Default Branch**: __YOUR_BRANCH_NAME__
- **Project Title**: __YOUR_PROJECT_TITLE__
- **Project Tagline**: __YOUR_PROJECT_TAGLINE__
- **Workspace Path**: __YOUR_WORKSPACE_PATH__

## Personal Information (for blog customization)
- **Your Name**: __YOUR_FULL_NAME__
- **Job Title**: __YOUR_JOB_TITLE__
- **GitHub Profile**: __YOUR_GITHUB_USERNAME__
- **Profile Image**: __PATH_TO_YOUR_IMAGE__ (optional)

## Requirements

### 1. Initialize Docusaurus
- Create a Docusaurus site in a `docs/` directory at the project root
- Use TypeScript template with classic preset
- Configure for GitHub Pages deployment at: `https://__YOUR_GITHUB_USERNAME__.github.io/__YOUR_REPO_NAME__/`

### 2. Configuration
Update `docs/docusaurus.config.ts` with:
- Set `title` to "__YOUR_PROJECT_TITLE__"
- Set `tagline` to "__YOUR_PROJECT_TAGLINE__"
- Set `url` to "https://__YOUR_GITHUB_USERNAME__.github.io"
- Set `baseUrl` to "/__YOUR_REPO_NAME__/"
- Set `organizationName` to "__YOUR_GITHUB_USERNAME__"
- Set `projectName` to "__YOUR_REPO_NAME__"
- Configure editUrl to point to the repository

### 3. Blog Customization
- Update `docs/blog/authors.yml` with my information:
  - Name: __YOUR_FULL_NAME__
  - Title: __YOUR_JOB_TITLE__
  - GitHub: __YOUR_GITHUB_USERNAME__
  - Image: __PATH_TO_YOUR_IMAGE__ (if provided)
- Customize welcome blog post with my profile
- Remove or update default blog posts

### 4. Documentation Structure
Create the following documentation pages:
- **Introduction** (`docs/docs/intro.md`): Project overview, quick start, prerequisites
- **Getting Started** (`docs/docs/guides/getting-started.md`): Installation, setup, running locally
- **Architecture** (`docs/docs/architecture/overview.md`): System architecture, tech stack
- Include instructions for running documentation locally: `cd __YOUR_WORKSPACE_PATH__/docs && npm start`

### 5. GitHub Actions Workflow
Create `.github/workflows/deploy-docs.yml` with:
- Trigger on push to `__YOUR_BRANCH_NAME__` branch
- Use Node.js 20.x and appropriate language versions if building APIs
- Build Docusaurus site
- Deploy to GitHub Pages using `peaceiris/actions-gh-pages@v3` or `actions/deploy-pages`
- Set proper permissions for GitHub Pages deployment

### 6. Navigation
Configure navigation in `docs/docusaurus.config.ts`:
- Add "Documentation" link to docs sidebar
- Add "Blog" link
- Add "GitHub" link to repository

### 7. Homepage
Update `docs/src/pages/index.tsx`:
- Set hero title to project title
- Set hero subtitle to project tagline
- Update "Get Started" button to link to documentation

### 8. Additional Files
Create supporting documentation:
- `DEPLOYMENT_GUIDE.md`: Step-by-step GitHub Pages setup instructions
- `README.md` updates: Add documentation link and badge

## Expected Deliverables

After completion, I should have:
1. ✅ Fully configured Docusaurus site in `docs/` directory
2. ✅ GitHub Actions workflow for automated deployment
3. ✅ Customized blog with my author profile
4. ✅ Documentation pages with project-specific content
5. ✅ Deployment guide with manual setup steps
6. ✅ All links properly configured (no broken links)
7. ✅ Local development command documented

## Post-Setup Manual Steps

After you complete the setup, remind me to:
1. Navigate to: https://github.com/__YOUR_GITHUB_USERNAME__/__YOUR_REPO_NAME__/settings/pages
2. Under "Build and deployment" → "Source", select **"GitHub Actions"**
3. Commit and push changes to trigger the workflow
4. Wait for deployment at: https://__YOUR_GITHUB_USERNAME__.github.io/__YOUR_REPO_NAME__/

## Important Notes
- Ensure all internal documentation links use proper paths (e.g., `/docs/guides/getting-started` for doc-to-doc links)
- Test for broken links before deployment
- Use Docusaurus version 3.x or latest stable
- Include proper .gitignore for node_modules and build artifacts

Please proceed with the setup step by step, asking for clarification if any placeholder values are unclear.
```

---

## 📝 Example: Filled Template

Here's an example with actual values (like the fintech-mapping-features project):

```
I need you to set up Docusaurus documentation with automated GitHub Pages deployment for my project.

## Project Information
- **GitHub Username/Org**: Ejyke90
- **Repository Name**: fintech-mapping-features
- **Default Branch**: main
- **Project Title**: Fintech Mapping Features
- **Project Tagline**: Multi-module Spring Boot Microservices for Fintech Data Transformation
- **Workspace Path**: /Users/ejikeudeze/AI_Projects/fintech-mapping-features

## Personal Information (for blog customization)
- **Your Name**: Ejike Udeze
- **Job Title**: Cloud Engineer and AI Enthusiast
- **GitHub Profile**: Ejyke90
- **Profile Image**: docs/blog/2021-08-26-welcome/Stage_Ejike_U.jpg

## Requirements

[... rest of the prompt remains the same ...]
```

---

## 🔧 Advanced Customization Options

### For Multi-Module Projects (like Spring Boot, Gradle, Maven)

Add this section to your prompt:

```
## Additional Requirements for Multi-Module Projects

My project is a multi-module [Spring Boot/Maven/Gradle/etc.] project with the following modules:
- **Module 1**: __MODULE_1_NAME__ (Port: __PORT_1__, Description: __DESCRIPTION_1__)
- **Module 2**: __MODULE_2_NAME__ (Port: __PORT_2__, Description: __DESCRIPTION_2__)

Additional tasks:
1. Install SpringDoc OpenAPI dependencies (if Spring Boot):
   - Add `springdoc-openapi-starter-webmvc-ui:2.3.0` to each module's build file
   - Configure OpenAPI endpoints in `application.properties`

2. Configure GitHub Actions workflow to:
   - Build all modules
   - Start services to extract OpenAPI specs
   - Download OpenAPI specs from running services
   - Generate API documentation with Docusaurus OpenAPI plugin

3. Install Docusaurus OpenAPI plugins:
   ```bash
   npm install docusaurus-plugin-openapi-docs docusaurus-theme-openapi-docs
   ```

4. Create module-specific documentation pages with API references
```

### For API Documentation with OpenAPI/Swagger

```
## API Documentation Requirements

My project exposes REST APIs. Please:
1. Install OpenAPI documentation plugins for Docusaurus
2. Configure OpenAPI spec locations in `docusaurus.config.ts`
3. Create API documentation pages for each service
4. Add Swagger UI integration
5. Document API endpoints with examples in markdown files
```

### For Monorepo Projects

```
## Monorepo Configuration

My project is a monorepo with multiple packages/services:
- Service locations: __LIST_SERVICE_PATHS__
- Build command: __BUILD_COMMAND__
- Test command: __TEST_COMMAND__

Please configure the workflow to:
1. Build all services in the correct order
2. Handle dependencies between services
3. Run tests before deployment
4. Generate documentation for each service
```

---

## 📊 Project Structure Reference

After AI completes the setup, your structure should look like:

```
your-project/
├── .github/
│   └── workflows/
│       └── deploy-docs.yml          # GitHub Actions workflow
├── docs/                             # Docusaurus site
│   ├── blog/
│   │   ├── authors.yml              # Your author profile
│   │   └── [blog-posts]/
│   ├── docs/
│   │   ├── intro.md                 # Homepage
│   │   ├── guides/
│   │   │   └── getting-started.md
│   │   ├── architecture/
│   │   │   └── overview.md
│   │   └── [other-docs]/
│   ├── src/
│   │   └── pages/
│   │       └── index.tsx            # Landing page
│   ├── static/
│   │   └── img/
│   ├── docusaurus.config.ts         # Main config
│   ├── sidebars.ts                  # Sidebar navigation
│   ├── package.json
│   └── tsconfig.json
├── [your-source-code]/
├── DEPLOYMENT_GUIDE.md              # Manual setup steps
└── README.md                        # Updated with docs link
```

---

## ✅ Verification Checklist

After AI completes the setup, verify:

- [ ] `npm start` works locally from docs directory
- [ ] All links are functional (no broken link errors)
- [ ] Blog shows your author profile
- [ ] GitHub Actions workflow file exists and is valid
- [ ] Documentation pages render correctly
- [ ] Navigation menu works
- [ ] Search functionality works (if enabled)
- [ ] Build command completes without errors: `cd docs && npm run build`
- [ ] Generated site is in `docs/build/` directory

---

## 🐛 Troubleshooting Common Issues

### Issue: "Docusaurus found broken links"
**Solution**: Ensure all internal links use proper paths:
- Doc-to-doc: `/docs/path/to/doc`
- To homepage: `/`
- To blog: `/blog/post-name`

### Issue: "GitHub Actions workflow fails"
**Solution**: Check:
1. Workflow has correct branch name
2. Node.js version matches local (use 20.x)
3. Build commands are correct
4. Permissions are set in workflow file

### Issue: "Site not deploying to GitHub Pages"
**Solution**: 
1. Verify GitHub Pages source is set to "GitHub Actions" (not "Deploy from a branch")
2. Check workflow run logs in Actions tab
3. Ensure workflow completed successfully

### Issue: "Custom domain not working"
**Solution**: Add CNAME file to `docs/static/` directory with your domain

---

## 📚 Additional Resources

- [Docusaurus Documentation](https://docusaurus.io/docs)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docusaurus OpenAPI Plugin](https://github.com/PaloAltoNetworks/docusaurus-openapi-docs)

---

## 💡 Tips for Best Results

1. **Be Specific**: Fill in ALL placeholders before giving to AI
2. **One Step at a Time**: Ask AI to confirm each major step before proceeding
3. **Review Changes**: Check generated files before committing
4. **Test Locally**: Always run `npm start` to verify before pushing
5. **Iterative Approach**: Start with basic setup, then add advanced features
6. **Version Control**: Commit after each major milestone
7. **Documentation First**: Focus on content structure before styling

---

## 🎯 Success Criteria

Your setup is complete when:
- ✅ Documentation site builds without errors
- ✅ GitHub Actions workflow runs successfully
- ✅ Site is accessible at `https://YOUR_USERNAME.github.io/YOUR_REPO/`
- ✅ All navigation links work
- ✅ Blog displays your profile correctly
- ✅ Local development works with hot reload
- ✅ API documentation is integrated (if applicable)

---

## 📄 License

This template is provided as-is for use in setting up documentation for any project.

---

**Last Updated**: October 2025  
**Docusaurus Version**: 3.9.1+  
**Node.js Version**: 20.x+  
**GitHub Actions**: Latest
