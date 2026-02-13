# File Structure

```
ib-options/
├── SKILL.md                 # AI assistant instructions (main entry point)
├── README.md               # User documentation
├── QUICKREF.md             # Quick command reference
├── INSTALL.md              # Installation guide
├── CUSTOMIZATION.md        # How to customize for your environment
├── LICENSE                 # MIT License
├── VERSION                 # Version number (1.0.0)
├── .gitignore              # Git ignore patterns
├── config.example.sh       # Example configuration file
│
├── scripts/
│   └── ib-options.py       # Main Python script
│
└── examples/
    ├── basic-usage.sh      # Basic usage examples
    └── put-selling-scan.sh # Watchlist scanner for put sellers
```

## File Purposes

### For AI Assistants

- **SKILL.md** - Read this first. Contains when to use the tool, common workflows, and tips.
- **QUICKREF.md** - Quick command syntax reference for generating commands.

### For Users

- **README.md** - Main user documentation with examples
- **INSTALL.md** - Setup instructions
- **CUSTOMIZATION.md** - How to adapt to your specific environment
- **QUICKREF.md** - Command cheat sheet

### Configuration

- **config.example.sh** - Template for environment-specific settings
- **scripts/ib-options.py** - The actual tool (customize defaults here)

### Examples

- **examples/*.sh** - Working example scripts demonstrating common use cases

### Meta

- **LICENSE** - MIT License (open source, reusable)
- **VERSION** - Current version number
- **.gitignore** - Files to exclude from version control
