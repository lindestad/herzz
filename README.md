# HERZZ Car Rental System - Git Training Workshop

**HERZZ**: **H**euristic **E**ngine for **R**ental **Z**one **Z**oning

## Project Overview

The HERZZ Car Rental System is a Python-based car rental management system designed specifically for Git training workshops. The system simulates real-world car rental operations and provides a practical environment for learning Git concepts, workflows, and collaboration techniques.

## Features

- **Car Management**: Add, track, and manage rental car inventory
- **Customer Management**: Handle customer registration and information
- **Rental Processing**: Process car rentals and returns
- **Location Management**: Support for multiple rental locations
- **Data Persistence**: JSON and CSV file support for data storage
- **Comprehensive Testing**: Unit tests for all major components
- **CI/CD Pipeline**: GitHub Actions workflow for automated testing and code quality

## Project Structure

```
herzz/
├── car_rental.py          # Main car rental system classes and logic
├── utils.py               # Utility functions for data handling
├── test_car_rental.py     # Comprehensive unit tests
├── data/                  # Sample data files
│   ├── rental_locations.json
│   ├── car_inventory.csv
│   └── customers.csv
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI/CD pipeline
├── .gitignore
└── README.md              # This file
```

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Git (for the training exercises)

### Running the System
```bash
# Clone the repository
git clone https://github.com/lindestad/herzz.git
cd herzz

# Run the main demo
python car_rental.py

# Run the tests
python test_car_rental.py
```

## Git Training Exercises

This repository is structured to provide hands-on experience with various Git concepts. The exercises are designed to be completed in order, building upon previous knowledge.

### Exercise 1: Basic Git Operations

**Objective**: Learn fundamental Git commands and local repository management.

**Tasks**:
1. Clone the repository locally
2. Explore the commit history
3. Check the status and current branch
4. Create and switch to a new branch
5. Make small changes and commit them
6. View differences between commits

**Commands to Practice**:
```bash
git clone <repository-url>
git log --oneline --graph --all
git status
git branch
git checkout -b my-feature-branch
git add .
git commit -m "Your commit message"
git diff
git diff HEAD~1
```

### Exercise 2: Branch Management and Merging

**Objective**: Understand branching strategies and merge operations.

**Branches Available**:
- `main`: Stable production code
- `feature/branch-1`: New inventory tracking feature (contains a bug)
- `bugfix/branch-1`: Critical bug fix for main branch

**Tasks**:
1. Switch between different branches
2. Compare differences between branches
3. Practice different merge strategies
4. Resolve merge conflicts (intentionally created)
5. Use rebase as an alternative to merging

**Commands to Practice**:
```bash
git checkout main
git checkout feature/branch-1
git diff main..feature/branch-1
git merge feature/branch-1
git rebase main
git log --oneline --graph --all
```

### Exercise 3: Conflict Resolution

**Objective**: Learn to identify and resolve merge conflicts.

**Setup**: The `feature/branch-1` and `bugfix/branch-1` branches have conflicting changes that will require manual resolution.

**Tasks**:
1. Attempt to merge conflicting branches
2. Identify conflict markers in files
3. Manually resolve conflicts
4. Test the resolution
5. Complete the merge

**Conflict Resolution Process**:
```bash
git checkout main
git merge feature/branch-1
# Conflict occurs - edit conflicted files
# Look for <<<<<<< HEAD, =======, and >>>>>>> markers
git add resolved-file.py
git commit -m "Resolved merge conflict"
```

### Exercise 4: Remote Repository Management

**Objective**: Practice working with remote repositories and collaboration workflows.

**Tasks**:
1. Add multiple remotes (simulate team collaboration)
2. Push to specific remotes
3. Fetch and pull from different remotes
4. Practice selective pushing
5. Handle divergent branches

**Commands to Practice**:
```bash
git remote -v
git remote add upstream <original-repo-url>
git remote add teammate <teammate-repo-url>
git fetch upstream
git push origin feature-branch
git pull upstream main
```

### Exercise 5: Advanced Git Operations

**Objective**: Explore advanced Git features and workflows.

**Tasks**:
1. Interactive rebase to clean up commit history
2. Cherry-pick specific commits
3. Use git stash for temporary changes
4. Create and apply patches
5. Use git bisect for debugging

**Commands to Practice**:
```bash
git rebase -i HEAD~3
git cherry-pick <commit-hash>
git stash
git stash pop
git format-patch HEAD~2
git bisect start
```

## Development Setup

### Installing Development Dependencies
```bash
pip install flake8 black isort pylint mypy bandit
```

### Code Quality Checks
```bash
# Format code
black .
isort .

# Lint code
flake8 .
pylint *.py

# Type checking
mypy *.py

# Security scanning
bandit -r .
```

## Testing

The project includes comprehensive unit tests to ensure code quality and functionality.

```bash
# Run all tests
python test_car_rental.py

# Run tests with verbose output
python test_car_rental.py -v
```

## Sample Data

The repository includes sample data to simulate a real car rental business:

- **5 Rental Locations**: From budget to luxury locations across California
- **20 Cars**: Various makes, models, and price points
- **10 Customers**: Sample customer database

## CI/CD Pipeline

The repository includes a GitHub Actions workflow that automatically:

- Runs tests on multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Checks code formatting with Black
- Validates import sorting with isort
- Performs linting with flake8
- Runs security scanning with bandit
- Executes type checking with mypy

## Intentional Issues for Learning

The repository contains intentional issues in different branches to facilitate learning:

### In `feature/branch-1`:
- **Bug**: Division by zero error in inventory calculation
- **Location**: `utils.py` in the `calculate_inventory_utilization()` function
- **Learning Goal**: Practice debugging and fixing issues in feature branches

### In `main` branch:
- **Bug**: Memory leak in car allocation
- **Location**: `car_rental.py` in the rental processing
- **Learning Goal**: Understand how bugs can exist in production code

## Learning Resources

### Git Commands Quick Reference

| Command                     | Description                        |
| --------------------------- | ---------------------------------- |
| `git status`                | Show working tree status           |
| `git log --oneline --graph` | Show commit history graphically    |
| `git branch -a`             | List all branches                  |
| `git checkout <branch>`     | Switch to branch                   |
| `git merge <branch>`        | Merge branch into current          |
| `git rebase <branch>`       | Rebase current branch onto another |
| `git cherry-pick <commit>`  | Apply specific commit              |
| `git stash`                 | Temporarily store changes          |

### Best Practices Demonstrated

1. **Commit Messages**: Clear, descriptive commit messages
2. **Branch Naming**: Consistent naming convention (feature/, bugfix/, hotfix/)
3. **Code Organization**: Modular structure with separate concerns
4. **Testing**: Comprehensive test coverage
5. **Documentation**: Clear README and inline documentation
6. **CI/CD**: Automated testing and quality checks

## Contributing

This project is designed for educational purposes. When completing exercises:

1. Create descriptive branch names
2. Write clear commit messages
3. Test your changes before committing
4. Follow the established code style
5. Document any new features or changes

## Exercise Solutions

### Common Patterns and Solutions

**Creating a feature branch**:
```bash
git checkout -b feature/my-new-feature
# Make changes
git add .
git commit -m "Add new feature: description"
git push origin feature/my-new-feature
```

**Fixing merge conflicts**:
```bash
git merge conflicting-branch
# Edit conflicted files, removing conflict markers
git add resolved-file.py
git commit -m "Resolve merge conflict between main and feature"
```

**Interactive rebase cleanup**:
```bash
git rebase -i HEAD~3
# In editor: pick, squash, or drop commits as needed
# Save and exit
```

## Learning Objectives

By completing these exercises, you will learn:

- Basic Git commands and repository management
- Branching strategies and workflows
- Merge conflict identification and resolution
- Remote repository collaboration
- Advanced Git operations and techniques
- Best practices for version control
- CI/CD pipeline integration with Git workflows

## Getting Help

If you encounter issues during the training:

1. Check the Git documentation: `git help <command>`
2. Review the commit history: `git log --oneline --graph`
3. Use `git status` to understand the current state
4. Consult the instructor or training materials
5. Practice in a safe environment (this repository is designed for experimentation)

---

This repository provides a safe environment to experiment with Git commands and learn version control best practices. Experimentation and learning from mistakes is encouraged as part of the training process.
