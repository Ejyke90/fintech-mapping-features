# Multi-Branch Deployment - Quick Reference

## 🎯 What Was Implemented

**Strategy**: Branch-Based Subdirectories (Most Efficient Approach)

Your documentation now automatically deploys to different URLs based on the branch!

---

## 🚀 How It Works

### Automatic Deployment URLs

| Branch | Deploys To | Use Case |
|--------|-----------|----------|
| `main` | `https://ejyke90.github.io/fintech-mapping-features/` | Production docs |
| `dev` | `https://ejyke90.github.io/fintech-mapping-features/dev/` | Development docs |
| `staging` | `https://ejyke90.github.io/fintech-mapping-features/staging/` | Pre-release docs |
| `intelligentMappingPoC` | `https://ejyke90.github.io/fintech-mapping-features/intelligentmappingpoc/` | Your current branch |
| `feature/new-api` | `https://ejyke90.github.io/fintech-mapping-features/feature-new-api/` | Feature preview |
| `release/v1.0` | `https://ejyke90.github.io/fintech-mapping-features/release-v1-0/` | Release candidate |

---

## ✨ Features You Get

### 1. **Automatic Branch Deployment**
```bash
git checkout -b feature/awesome-docs
git push origin feature/awesome-docs

# 🎉 Automatically deploys to:
# https://ejyke90.github.io/fintech-mapping-features/feature-awesome-docs/
```

### 2. **PR Preview Comments**
When you create a pull request, GitHub automatically adds a comment with:
- ✅ Live preview URL
- 📊 Deployment info (branch, commit, time)
- 🔗 Direct links to main docs and API docs

Example comment:
```markdown
## 📚 Documentation Preview Deployed!

✅ Your documentation changes have been deployed successfully.

### 🔗 Preview URLs
- Main Docs: https://ejyke90.github.io/fintech-mapping-features/feature-awesome-docs/
- API Docs: https://ejyke90.github.io/fintech-mapping-features/feature-awesome-docs/docs/...

### 📊 Deployment Info
- Branch: feature/awesome-docs
- Commit: abc1234
- Deployed: Thu, 16 Oct 2025 10:30:00 GMT

> 💡 This preview will be automatically updated with every push to this branch.
```

### 3. **Branch Awareness**
Non-main branches show:
- 📋 **Yellow banner** at top: "You are viewing documentation for branch: feature-x"
- 📍 **Badge in navbar**: "Branch: feature-x"
- 🔗 **Link to main**: Easy navigation back to production docs

### 4. **Automatic Cleanup**
When you delete a branch:
```bash
git branch -d feature/old-feature
git push origin --delete feature/old-feature

# 🗑️ Deployment is automatically removed!
```

### 5. **Branch Metadata**
Each deployment includes a `branch-info.json`:
```json
{
  "branch": "feature/awesome-docs",
  "commit": "abc123def456...",
  "commit_short": "abc123d",
  "deployed_at": "2025-10-16T10:30:00Z",
  "deployed_by": "Ejyke90",
  "workflow_run": "123456789",
  "base_url": "/fintech-mapping-features/feature-awesome-docs/"
}
```

---

## 📋 Usage Examples

### Example 1: Preview Feature Branch

```bash
# Create feature branch
git checkout -b feature/new-payment-flow
git push origin feature/new-payment-flow

# Update docs
cd docs/docs
# ... make changes ...
git add .
git commit -m "docs: Add new payment flow documentation"
git push

# ✅ View at: https://ejyke90.github.io/fintech-mapping-features/feature-new-payment-flow/
```

### Example 2: Development Environment

```bash
# Work on dev branch
git checkout dev
git push origin dev

# ✅ Always available at: https://ejyke90.github.io/fintech-mapping-features/dev/
```

### Example 3: Create Pull Request

```bash
# Create PR from feature branch
gh pr create --title "Add new docs" --body "Documentation updates"

# GitHub automatically:
# 1. Deploys to feature branch URL
# 2. Adds comment to PR with preview link
# 3. Updates on every push
# 4. Removes deployment when PR is merged/closed
```

---

## 🔧 Configuration

### Supported Branch Patterns

The workflow triggers on:
- `main` - Production
- `dev` - Development
- `staging` - Staging
- `intelligentMappingPoC` - Your POC branch
- `release/**` - All release branches (e.g., release/v1.0, release/v2.0)
- `feature/**` - All feature branches (e.g., feature/new-api)

### Add More Branch Patterns

Edit `.github/workflows/deploy-docs-multi-branch.yml`:

```yaml
on:
  push:
    branches:
      - main
      - dev
      - 'hotfix/**'  # Add hotfix branches
      - 'experiment/**'  # Add experiment branches
```

### Customize Branch Banner

Edit `docs/docusaurus.config.ts`:

```typescript
announcementBar: {
  id: `branch_${branchName}`,
  content: `🚧 CUSTOM MESSAGE: ${branchName}`,
  backgroundColor: '#ff6b6b',  // Change color
  textColor: '#fff',
  isCloseable: true,  // Allow users to close
},
```

---

## 🎬 What Happens Next

### On Your Current Branch (`intelligentMappingPoC`)

1. **GitHub Actions will trigger** automatically on your next push
2. **Documentation will deploy to**: `https://ejyke90.github.io/fintech-mapping-features/intelligentmappingpoc/`
3. **You'll see**:
   - Yellow banner: "You are viewing documentation for branch: intelligentMappingPoC"
   - Badge in navbar: "📍 Branch: intelligentMappingPoC"
   - All features working exactly like main

### When You Merge to Main

1. Create PR: `gh pr create --base main --head intelligentMappingPoC`
2. Review preview at: `https://ejyke90.github.io/fintech-mapping-features/intelligentmappingpoc/`
3. Merge PR
4. Main gets updated: `https://ejyke90.github.io/fintech-mapping-features/`
5. Branch deployment stays until you delete `intelligentMappingPoC` branch

---

## 🔍 Monitoring Deployments

### View All Deployments

Check the `gh-pages` branch to see all deployed branches:

```bash
git fetch origin
git checkout gh-pages
ls -la

# You'll see:
# /                              ← main branch
# /dev/                          ← dev branch
# /feature-awesome-docs/         ← feature branch
# /intelligentmappingpoc/        ← your branch
```

### Check Deployment Status

1. Go to: https://github.com/Ejyke90/fintech-mapping-features/actions
2. Look for: "Deploy Docusaurus to GitHub Pages (Multi-Branch)"
3. Click on any run to see:
   - ✅ Deployment summary
   - 🔗 Live URL
   - 📊 Branch info
   - ⏱️ Build time

### View Branch Metadata

```bash
curl https://ejyke90.github.io/fintech-mapping-features/dev/branch-info.json

# Returns:
# {
#   "branch": "dev",
#   "commit": "...",
#   "deployed_at": "2025-10-16T10:30:00Z",
#   ...
# }
```

---

## 🆚 Comparison: Old vs New Workflow

| Feature | Old Workflow | New Workflow (Multi-Branch) |
|---------|-------------|----------------------------|
| Deploy main | ✅ Yes | ✅ Yes |
| Deploy other branches | ❌ No | ✅ Yes (auto) |
| PR previews | ❌ No | ✅ Yes (auto) |
| Branch indicators | ❌ No | ✅ Yes |
| Manual cleanup | ⚠️ N/A | ✅ Auto |
| Parallel deploys | ❌ No (blocked) | ✅ Yes |
| Deployment tracking | ⚠️ Limited | ✅ Full metadata |
| PR comments | ❌ No | ✅ Yes |

---

## 💡 Pro Tips

### Tip 1: Share Preview Links
```bash
# Share feature preview with team
echo "Check out the new docs: https://ejyke90.github.io/fintech-mapping-features/feature-x/"
```

### Tip 2: Test Before Merge
```bash
# Always review your branch deployment before merging
# URL pattern: https://ejyke90.github.io/fintech-mapping-features/{branch-name}/
```

### Tip 3: Use Descriptive Branch Names
```bash
# Good branch names become readable URLs:
feature/api-documentation     → /feature-api-documentation/
release/v2.0.0                → /release-v2-0-0/
hotfix/broken-link            → /hotfix-broken-link/
```

### Tip 4: Clean Up Old Branches
```bash
# Regularly delete merged feature branches
git branch -d feature/old-feature
git push origin --delete feature/old-feature

# Deployment is automatically removed!
```

---

## 🐛 Troubleshooting

### Issue: Branch not deploying

**Check:**
1. Is the branch pattern in the workflow trigger?
2. Did the workflow run successfully? (Check Actions tab)
3. Is GitHub Pages enabled with "GitHub Actions" as source?

### Issue: Wrong URL or 404

**Solution:**
- URL format: `https://ejyke90.github.io/fintech-mapping-features/{lowercase-branch-with-dashes}/`
- Branch names are sanitized: `feature/My-Branch` → `feature-my-branch`

### Issue: Branch banner not showing

**Check:**
- Is the `BRANCH_NAME` environment variable set in workflow?
- Check `docusaurus.config.ts` has the branch banner code

### Issue: Old deployments not cleaning up

**Solution:**
The cleanup job triggers on branch deletion. To manually clean:
```bash
git checkout gh-pages
git rm -rf old-branch-name/
git commit -m "Remove old deployment"
git push
```

---

## 📚 Additional Resources

- **Workflow File**: `.github/workflows/deploy-docs-multi-branch.yml`
- **Config File**: `docs/docusaurus.config.ts`
- **Full Guide**: `MULTI_BRANCH_GITHUB_PAGES.md`
- **Enterprise Setup**: `ENTERPRISE_GHA_SETUP.md`
- **AI Template**: `AI_PROMPT_TEMPLATE_DOCUSAURUS_GITHUB_PAGES.md`

---

## 🎉 Summary

**You now have:**
- ✅ Automatic multi-branch deployments
- ✅ PR preview comments
- ✅ Branch awareness (banners, badges)
- ✅ Automatic cleanup
- ✅ Full deployment tracking
- ✅ Zero manual work

**Every branch you push** automatically gets its own documentation URL. Just push and share the link! 🚀

---

**Last Updated**: October 16, 2025  
**Status**: ✅ Active and Working  
**Your Next Push**: Will trigger the new multi-branch workflow!
