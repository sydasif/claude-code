#!/bin/bash

# ASCII mode: set CLAUDE_STATUSLINE_ASCII=1 for ASCII-only output (no emojis)
# Example: export CLAUDE_STATUSLINE_ASCII=1 in your shellrc

# Define ANSI color codes as variables
RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'
PURPLE=$'\033[0;35m'
CYAN=$'\033[0;36m'
WHITE=$'\033[1;37m'
NC=$'\033[0m' # No Color

# Emoji or ASCII fallback
if [ "${CLAUDE_STATUSLINE_ASCII:-0}" = "1" ]; then
    DIR_ICON="[D]"
    BRAIN_ICON="[M]"
    BRANCH_ICON="[*]"
    STAGED_PLUS="+"
    UNSTAGED_TILDE="~"
    UNTRACKED_Q="?"
else
    DIR_ICON="📁"
    BRAIN_ICON="🧠"
    BRANCH_ICON="🌿"
    STAGED_PLUS="+"
    UNSTAGED_TILDE="~"
    UNTRACKED_Q="?"
fi

# Read the input JSON from stdin
input=$(cat)

# Extract information from the JSON
dir=$(echo "$input" | jq -r '.workspace.current_dir | split("/")[-1]')
model=$(echo "$input" | jq -r '.model.display_name')
pwd_path=$(echo "$input" | jq -r '.workspace.current_dir')

# Format the path for display
if [ "$pwd_path" = "$HOME" ]; then
    display_path="~"
elif [[ "$pwd_path" = "$HOME/"* ]]; then
    display_path="~/$(echo "$pwd_path" | sed "s|$HOME/||")"
else
    display_path="$pwd_path"
fi

# Get git status information if in a git repository
git_info=""
if command -v git >/dev/null 2>&1; then
    # Run git status with --no-optional-locks to avoid potential lock issues
    # Use pushd/popd instead of cd to avoid changing the current directory permanently
    git_status=$(cd "$pwd_path" 2>/dev/null && git --no-optional-locks status --porcelain 2>/dev/null || echo "")
    git_branch=$(cd "$pwd_path" 2>/dev/null && git --no-optional-locks rev-parse --abbrev-ref HEAD 2>/dev/null || echo "")

    if [ -n "$git_branch" ] && [ "$git_branch" != "HEAD" ]; then
        # Count changes, ensuring we get a numeric value
        if [ -n "$git_status" ]; then
            staged_count=$(echo "$git_status" | grep -c '^[^ ?]' 2>/dev/null)
            unstaged_count=$(echo "$git_status" | grep -v '^??' | grep -c '^.[^ ]' 2>/dev/null)
            untracked_count=$(echo "$git_status" | grep -c '^??' 2>/dev/null)

            # Ensure counts are numeric (in case grep -c returns error)
            staged_count=$(echo "$staged_count" | tr -cd '0-9')
            [ -z "$staged_count" ] && staged_count=0
            unstaged_count=$(echo "$unstaged_count" | tr -cd '0-9')
            [ -z "$unstaged_count" ] && unstaged_count=0
            untracked_count=$(echo "$untracked_count" | tr -cd '0-9')
            [ -z "$untracked_count" ] && untracked_count=0
        else
            staged_count=0
            unstaged_count=0
            untracked_count=0
        fi

        # Format git info with colors
        git_info="${GREEN}${BRANCH_ICON} ${CYAN}$git_branch"
        if [ "$staged_count" -gt 0 ]; then
            git_info="$git_info ${GREEN}${STAGED_PLUS}$staged_count"
        fi
        if [ "$unstaged_count" -gt 0 ]; then
            git_info="$git_info ${YELLOW}${UNSTAGED_TILDE}$unstaged_count"
        fi
        if [ "$untracked_count" -gt 0 ]; then
            git_info="$git_info ${RED}${UNTRACKED_Q}$untracked_count"
        fi
        git_info="$git_info"
    fi
fi

# Output the formatted status line
if [ -n "$git_info" ]; then
    printf "${CYAN}${DIR_ICON} ${WHITE}%s${NC} | ${PURPLE}${BRAIN_ICON} ${YELLOW}%s${NC} | %s${NC}\n" "$display_path" "$model" "$git_info"
else
    printf "${CYAN}${DIR_ICON} ${WHITE}%s${NC} | ${PURPLE}${BRAIN_ICON} ${YELLOW}%s${NC}\n" "$display_path" "$model"
fi