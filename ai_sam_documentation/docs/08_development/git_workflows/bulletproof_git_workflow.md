# Bulletproof Git Workflow - Safe Development with Nuclear Rollback

## The Problem You're Solving
- ✅ **Good session**: Want to commit and push progress to GitHub
- ❌ **Bad session**: Want to completely nuke everything and start fresh from GitHub
- 🔄 **Experimentation**: Need safe space to try risky changes with Claude Code

## Git Workflow Strategy

### Branch Structure
```
main (production)
├── stable (known working version)
├── consolidation (current major work)
└── experiment-YYYYMMDD (daily experiment branches)
```

## Phase 1: Safe Experimentation Setup

### Daily Experiment Branch
```bash
# Before EVERY Claude Code session
git checkout stable
git pull origin stable
git checkout -b experiment-$(date +%Y%m%d)
git push -u origin experiment-$(date +%Y%m%d)
```

**What this gives you:**
- ✅ **Clean starting point** - Always start from known good state
- ✅ **Isolated changes** - Claude Code changes don't affect main code
- ✅ **Easy rollback** - Just delete the experiment branch
- ✅ **Traceable** - Date-stamped branches show what you tried when

## Phase 2: Session Management

### Starting a Development Session
```bash
#!/bin/bash
# save as: start_session.sh

echo "🚀 Starting new development session..."

# Ensure we're on stable branch
git checkout stable
git pull origin stable

# Create new experiment branch
BRANCH_NAME="experiment-$(date +%Y%m%d-%H%M)"
git checkout -b $BRANCH_NAME
git push -u origin $BRANCH_NAME

echo "✅ Created experiment branch: $BRANCH_NAME"
echo "🎯 Safe to make changes. Rollback available anytime."
echo ""
echo "📋 Session commands:"
echo "  Good session: ./promote_session.sh"
echo "  Bad session:  ./nuclear_rollback.sh"
```

### Good Session - Promote Changes
```bash
#!/bin/bash
# save as: promote_session.sh

echo "🎉 Promoting successful session..."

# Get current experiment branch name
CURRENT_BRANCH=$(git branch --show-current)

# Make sure all changes are committed
git add .
git commit -m "Session completed: $(date)"
git push origin $CURRENT_BRANCH

# Merge to stable branch
git checkout stable
git merge $CURRENT_BRANCH --no-ff -m "Merged successful session: $CURRENT_BRANCH"
git push origin stable

# Optional: merge to main for production
read -p "📦 Promote to main branch? (y/N): " promote_main
if [[ $promote_main =~ ^[Yy]$ ]]; then
    git checkout main
    git merge stable --no-ff -m "Production release: $(date)"
    git push origin main
    echo "🚀 Changes promoted to production!"
fi

# Clean up experiment branch
git branch -d $CURRENT_BRANCH
git push origin --delete $CURRENT_BRANCH

echo "✅ Session successfully promoted and cleaned up!"
```

### Bad Session - Nuclear Rollback
```bash
#!/bin/bash
# save as: nuclear_rollback.sh

echo "💥 NUCLEAR ROLLBACK - Destroying all changes..."

# Get current experiment branch name
CURRENT_BRANCH=$(git branch --show-current)

# Safety check
echo "⚠️  This will DELETE ALL changes in branch: $CURRENT_BRANCH"
read -p "Are you ABSOLUTELY sure? Type 'NUKE' to confirm: " confirm

if [ "$confirm" != "NUKE" ]; then
    echo "❌ Rollback cancelled"
    exit 1
fi

# Return to stable branch
git checkout stable

# Delete experiment branch locally
git branch -D $CURRENT_BRANCH

# Delete experiment branch on GitHub
git push origin --delete $CURRENT_BRANCH

# Force clean working directory
git reset --hard HEAD
git clean -fd

# Pull latest stable to ensure we're current
git pull origin stable

echo "🔥 NUCLEAR ROLLBACK COMPLETE!"
echo "✅ Returned to last known good state"
echo "🆕 Ready for fresh start"
```

## Phase 3: Milestone Management

### Creating Stable Milestones
```bash
#!/bin/bash
# save as: create_milestone.sh

MILESTONE_NAME=$1
if [ -z "$MILESTONE_NAME" ]; then
    echo "Usage: ./create_milestone.sh 'milestone-name'"
    exit 1
fi

echo "🏆 Creating milestone: $MILESTONE_NAME"

# Make sure we're on stable with latest changes
git checkout stable
git pull origin stable

# Create milestone tag
git tag -a "milestone-$MILESTONE_NAME" -m "Milestone: $MILESTONE_NAME - $(date)"
git push origin "milestone-$MILESTONE_NAME"

# Create milestone branch for reference
git checkout -b "milestone-$MILESTONE_NAME"
git push -u origin "milestone-$MILESTONE_NAME"
git checkout stable

echo "✅ Milestone created!"
echo "📌 Tag: milestone-$MILESTONE_NAME"
echo "🌿 Branch: milestone-$MILESTONE_NAME"
```

### Rollback to Any Milestone
```bash
#!/bin/bash
# save as: rollback_to_milestone.sh

# Show available milestones
echo "📌 Available milestones:"
git tag -l "milestone-*"
echo ""

read -p "Enter milestone name (without 'milestone-' prefix): " milestone

if [ -z "$milestone" ]; then
    echo "❌ No milestone specified"
    exit 1
fi

MILESTONE_TAG="milestone-$milestone"

# Check if milestone exists
if ! git tag -l | grep -q "^$MILESTONE_TAG$"; then
    echo "❌ Milestone not found: $MILESTONE_TAG"
    exit 1
fi

echo "⚠️  This will reset to milestone: $MILESTONE_TAG"
read -p "Are you sure? Type 'RESET' to confirm: " confirm

if [ "$confirm" != "RESET" ]; then
    echo "❌ Rollback cancelled"
    exit 1
fi

# Reset to milestone
git checkout stable
git reset --hard $MILESTONE_TAG
git push origin stable --force-with-lease

echo "🔄 Rolled back to milestone: $MILESTONE_TAG"
```

## Phase 4: Integration with Claude Code

### Claude Code Session Wrapper
```bash
#!/bin/bash
# save as: claude_code_session.sh

echo "🤖 Starting Claude Code session with safety net..."

# Start new experiment branch
./start_session.sh

echo ""
echo "🎯 Claude Code Safety Guidelines:"
echo "  1. Work in current experiment branch only"
echo "  2. Test changes frequently"
echo "  3. Commit good progress points"
echo "  4. Use refactoring tools in dev_tools/"
echo ""
echo "When done:"
echo "  ✅ Good session: ./promote_session.sh"
echo "  ❌ Bad session: ./nuclear_rollback.sh"
echo ""

# Optional: Start Claude Code automatically
read -p "Start Claude Code now? (y/N): " start_claude
if [[ $start_claude =~ ^[Yy]$ ]]; then
    claude-code
fi
```

## Daily Workflow Examples

### Scenario 1: Successful Consolidation Session
```bash
# Morning: Start fresh
./start_session.sh

# Work with Claude Code on consolidation
# ... Claude Code makes changes ...
# ... Test and verify changes work ...

# End of day: Everything works great
git add .
git commit -m "Successful consolidation: merged 3 canvas files into canvas_manager.js"
./promote_session.sh

# Result: Changes promoted to stable, experiment branch cleaned up
```

### Scenario 2: Disastrous Claude Code Session
```bash
# Morning: Start fresh
./start_session.sh

# Work with Claude Code
# ... Claude Code breaks everything ...
# ... Files are renamed incorrectly ...
# ... Imports are broken ...
# ... Nothing works ...

# Immediate response: Nuclear option
./nuclear_rollback.sh

# Result: Back to exactly where you started, like nothing happened
```

### Scenario 3: Major Milestone Achievement
```bash
# You've completed node overlay system successfully
./create_milestone.sh "node-overlay-complete"

# Continue working on next feature
./start_session.sh

# Later: Something goes wrong, want to go back to milestone
./rollback_to_milestone.sh
# Enter: node-overlay-complete

# Result: Back to the milestone state
```

## Repository Structure
```
your-repo/
├── .git/
├── addons/n8n_integration/           # Your actual module
├── dev_tools/                        # Refactoring tools
├── git_workflows/                    # Workflow scripts
│   ├── start_session.sh
│   ├── promote_session.sh
│   ├── nuclear_rollback.sh
│   ├── create_milestone.sh
│   ├── rollback_to_milestone.sh
│   └── claude_code_session.sh
└── README.md
```

## Setup Instructions

### 1. Create Workflow Scripts
```bash
mkdir git_workflows
cd git_workflows
# Copy all the bash scripts above
chmod +x *.sh
```

### 2. Initialize Branch Structure
```bash
# Ensure you're on main with latest code
git checkout main
git pull origin main

# Create stable branch
git checkout -b stable
git push -u origin stable

# Set stable as default development branch
git checkout stable
```

### 3. Test Workflow
```bash
# Test experiment branch creation
./start_session.sh

# Make a small test change
echo "# Test change" >> test.txt
git add test.txt
git commit -m "Test change"

# Test promotion
./promote_session.sh

# Test nuclear rollback
./start_session.sh
echo "# Bad change" >> bad.txt
./nuclear_rollback.sh

# Verify you're back to clean state
```

## Benefits

### Risk-Free Development
- ✅ **Always have escape hatch** - Nuclear rollback available anytime
- ✅ **Experiment safely** - Changes isolated in experiment branches
- ✅ **Milestone checkpoints** - Return to any known good state
- ✅ **Clean history** - Failed experiments don't pollute main branch

### Claude Code Integration
- ✅ **Contained damage** - Claude Code can't break your main code
- ✅ **Easy recovery** - One command to undo everything
- ✅ **Trackable sessions** - Each experiment is documented
- ✅ **Promotion workflow** - Only good changes make it to stable

This gives you the confidence to experiment aggressively with Claude Code, knowing you can always get back to safety!