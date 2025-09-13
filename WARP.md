# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a **Blockchain-Based Digital Certification System** - a Python-based application designed to generate, distribute, and validate digital certificates using blockchain technology. The system consists of multiple modular components for certificate generation, email distribution, blockchain integration, validation, and administrative functions.

## Development Commands

### Running the Email Distribution System
```powershell
# Navigate to email distribution module
cd src/email_dist

# Run the interactive certificate distribution system
python main.py
```

### Database Setup
```powershell
# Initialize the SQLite database (run once)
cd src/email_dist
python database_setup.py
```

### Testing Email Connection
The email distribution system includes built-in connection testing through the interactive menu (option 5) when running `main.py`.

## Architecture Overview

### Core Components Structure

The system follows a **modular architecture** with separate concerns:

1. **Email Distribution System** (`src/email_dist/`) - The only currently implemented module
2. **Certificate Generation** (`src/cert_gen/`) - Planned module for PDF certificate generation
3. **Blockchain Integration** (`src/blockchain/`) - Planned module for smart contracts and web3.py integration
4. **Validation Portal** (`src/validation_portal/`) - Planned Flask-based verification system
5. **Admin Dashboard** (`src/dashboard/`) - Planned analytics and management interface

### Email Distribution System Architecture

The implemented email distribution system uses a **layered architecture**:

- **`main.py`**: Interactive CLI interface and user interaction layer
- **`certificate_distributor.py`**: Core business logic orchestrating email and database operations
- **`email_service.py`**: Gmail API integration with OAuth2 authentication
- **`database_operations.py`**: SQLite database operations and data access layer
- **`database_setup.py`**: Database schema initialization and setup

### Database Schema

The system uses SQLite with two main tables:
- **`participants`**: Stores recipient information (name, email, organization, phone)
- **`certificates`**: Tracks certificate records with sending status, error handling, and email content

### Authentication & Credentials

The email system uses **Google OAuth2** for Gmail API access:
- Requires `credentials.json` (Google Cloud Console OAuth2 credentials)
- Automatically generates and stores `token.json` for persistent authentication
- Implements token refresh handling

## Key Dependencies

Based on code analysis, the project requires:
- `google-auth`
- `google-auth-oauthlib` 
- `google-auth-httplib2`
- `google-api-python-client`
- `sqlite3` (built-in Python)
- Standard Python libraries: `os`, `base64`, `email`, `datetime`, `typing`

## Development Workflow

- Work in feature branches
- Push code → Open Pull Request → Merge to `dev` branch
- After testing, merge `dev` → `main`

## Important Notes

### File Structure Expectations
- Certificate PDFs should be placed in `certificates/` directory (auto-created by database setup)
- Email credentials file must be named `credentials.json` in the email_dist directory
- Database file `certificates.db` is created automatically in the email_dist directory

### Email System Features
- **Batch Processing**: Can queue and send multiple certificates
- **Error Handling**: Tracks failed sends with error messages
- **Status Tracking**: Maintains pending/sent/failed status for all certificates
- **Interactive CLI**: Provides menu-driven interface for all operations
- **Statistics**: Built-in reporting for certificate distribution metrics

### Current Limitations
- Only the email distribution system is implemented
- Other modules (blockchain, cert_gen, validation_portal, dashboard) contain only placeholder `.gitkeep` files
- No automated testing framework is currently in place
- Requirements.txt is empty and needs to be populated with actual dependencies

## Future Development Areas

When implementing the remaining modules:
- **Certificate Generation**: Will likely use libraries like `reportlab` or `fpdf` for PDF generation
- **Blockchain Integration**: Will use `web3.py` for Ethereum interaction and smart contract deployment
- **Validation Portal**: Flask-based web application for certificate verification
- **Dashboard**: Administrative interface for analytics and bulk operations