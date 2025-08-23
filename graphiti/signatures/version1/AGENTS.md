# AGENTS.md

This file provides guidance to AI agents when working with version 1 signatures and CLA (Contributor License Agreement) data.

## Directory Overview

This directory contains type signatures and legal documentation for Graphiti API version 1, including contributor license agreement data.

## Files

- `cla.json` - Contributor License Agreement data and signatures

## Version 1 Specifications

### API Version 1

This version represents the stable API specification for Graphiti version 1.x:

1. **Core Interfaces**: Basic graph operations and data models
2. **Search APIs**: Entity and relationship search functionality
3. **Episode Management**: Episode creation and management
4. **Provider Interfaces**: LLM and embedding provider abstractions
5. **Configuration**: Configuration and setup interfaces

### CLA Management

The `cla.json` file contains contributor license agreement information:

#### CLA Data Structure

```json
{
  "version": "1.0",
  "agreement_text": "...",
  "contributors": [
    {
      "name": "Contributor Name",
      "email": "contributor@example.com",
      "signature_date": "2024-01-01",
      "agreement_version": "1.0"
    }
  ],
  "maintainers": [
    {
      "name": "Maintainer Name",
      "role": "Project Lead",
      "signature_date": "2024-01-01"
    }
  ]
}
```

## Agent Guidelines

### CLA Compliance

1. **Contributor Verification**: Check that contributors have signed CLA
2. **Legal Compliance**: Ensure all contributions comply with licensing terms
3. **Record Keeping**: Maintain accurate CLA records
4. **Version Tracking**: Track CLA versions and updates
5. **Automated Checking**: Implement automated CLA verification

### Working with CLA Data

#### Verification Process

```python
import json
from typing import List, Dict, Optional
from datetime import datetime

class CLAManager:
    """Manage Contributor License Agreement data."""
    
    def __init__(self, cla_file_path: str):
        self.cla_file_path = cla_file_path
        self.cla_data = self.load_cla_data()
    
    def load_cla_data(self) -> Dict:
        """Load CLA data from JSON file."""
        with open(self.cla_file_path, 'r') as f:
            return json.load(f)
    
    def is_contributor_signed(self, email: str) -> bool:
        """Check if contributor has signed CLA."""
        contributors = self.cla_data.get('contributors', [])
        return any(c['email'] == email for c in contributors)
    
    def add_contributor_signature(self, name: str, email: str) -> None:
        """Add new contributor signature."""
        new_contributor = {
            "name": name,
            "email": email,
            "signature_date": datetime.now().isoformat(),
            "agreement_version": self.cla_data.get('version', '1.0')
        }
        
        self.cla_data.setdefault('contributors', []).append(new_contributor)
        self.save_cla_data()
    
    def save_cla_data(self) -> None:
        """Save CLA data to file."""
        with open(self.cla_file_path, 'w') as f:
            json.dump(self.cla_data, f, indent=2)
    
    def generate_cla_report(self) -> Dict:
        """Generate CLA compliance report."""
        contributors = self.cla_data.get('contributors', [])
        return {
            "total_contributors": len(contributors),
            "cla_version": self.cla_data.get('version', 'unknown'),
            "recent_signatures": [
                c for c in contributors 
                if datetime.fromisoformat(c['signature_date']) > 
                   datetime.now() - timedelta(days=30)
            ]
        }
```

#### GitHub Integration

```python
# GitHub workflow integration
def check_pr_cla_compliance(pr_author_email: str) -> bool:
    """Check if PR author has signed CLA."""
    cla_manager = CLAManager('signatures/version1/cla.json')
    return cla_manager.is_contributor_signed(pr_author_email)

# GitHub Action example
def github_cla_check():
    """GitHub Action to check CLA compliance."""
    pr_author = os.getenv('PR_AUTHOR')
    pr_email = os.getenv('PR_AUTHOR_EMAIL')
    
    if not check_pr_cla_compliance(pr_email):
        print(f"❌ CLA not signed by {pr_author}")
        print("Please sign the Contributor License Agreement")
        sys.exit(1)
    else:
        print(f"✅ CLA signed by {pr_author}")
```

### API Version Management

#### Version 1 Interfaces

```python
# Core API interfaces for version 1
from typing import Protocol, List, Optional, Dict, Any
from datetime import datetime

class GraphitiV1Protocol(Protocol):
    """Graphiti API version 1 protocol."""
    
    async def add_episode(
        self,
        name: str,
        content: str,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Add episode to knowledge graph."""
        ...
    
    async def search_nodes(
        self,
        query: str,
        entity_types: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for entity nodes."""
        ...
    
    async def search_edges(
        self,
        query: str,
        relationship_types: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for relationship edges."""
        ...

class EmbedderV1Protocol(Protocol):
    """Embedder API version 1 protocol."""
    
    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for text."""
        ...
    
    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        ...
    
    @property
    def dimensions(self) -> int:
        """Get embedding dimensions."""
        ...
```

#### Backward Compatibility

```python
class APIVersionManager:
    """Manage API version compatibility."""
    
    def __init__(self):
        self.supported_versions = ['1.0', '1.1', '1.2']
        self.current_version = '1.2'
    
    def is_version_supported(self, version: str) -> bool:
        """Check if API version is supported."""
        return version in self.supported_versions
    
    def get_compatibility_adapter(self, from_version: str):
        """Get adapter for version compatibility."""
        if from_version == '1.0':
            return V1_0_to_Current_Adapter()
        elif from_version == '1.1':
            return V1_1_to_Current_Adapter()
        else:
            return None
```

### Legal Compliance

#### CLA Text Management

```python
def get_cla_text(version: str = "1.0") -> str:
    """Get CLA text for specified version."""
    cla_texts = {
        "1.0": """
        Contributor License Agreement (CLA) Version 1.0
        
        By signing this CLA, you agree that your contributions
        to this project will be licensed under the project's
        license terms.
        
        [Full legal text would be here]
        """
    }
    
    return cla_texts.get(version, cla_texts["1.0"])

def validate_cla_signature(signature_data: Dict) -> bool:
    """Validate CLA signature data."""
    required_fields = ['name', 'email', 'signature_date', 'agreement_version']
    
    for field in required_fields:
        if field not in signature_data:
            return False
    
    # Validate email format
    email = signature_data['email']
    if '@' not in email or '.' not in email.split('@')[1]:
        return False
    
    # Validate date format
    try:
        datetime.fromisoformat(signature_data['signature_date'])
    except ValueError:
        return False
    
    return True
```

#### License Compatibility

```python
def check_license_compatibility(license_type: str) -> bool:
    """Check if license is compatible with project."""
    compatible_licenses = [
        'MIT',
        'Apache-2.0',
        'BSD-3-Clause',
        'ISC'
    ]
    
    return license_type in compatible_licenses

def analyze_contribution_licensing(contribution_path: str) -> Dict:
    """Analyze licensing of contribution."""
    # Scan for license headers
    # Check for incompatible license terms
    # Return licensing analysis
    return {
        "has_license_header": True,
        "license_type": "MIT",
        "compatible": True,
        "issues": []
    }
```

### Automated Compliance

#### CI/CD Integration

```yaml
# GitHub Action for CLA checking
name: CLA Check

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  cla-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Check CLA Signature
      run: |
        python scripts/check_cla.py \
          --author "${{ github.event.pull_request.user.login }}" \
          --email "${{ github.event.pull_request.user.email }}"
```

#### CLA Bot Integration

```python
class CLABot:
    """Automated CLA management bot."""
    
    def __init__(self, github_token: str):
        self.github = Github(github_token)
        self.cla_manager = CLAManager('signatures/version1/cla.json')
    
    def handle_pull_request(self, pr_data: Dict) -> None:
        """Handle new pull request CLA check."""
        author_email = pr_data['author_email']
        
        if not self.cla_manager.is_contributor_signed(author_email):
            self.request_cla_signature(pr_data)
        else:
            self.approve_cla_check(pr_data)
    
    def request_cla_signature(self, pr_data: Dict) -> None:
        """Request CLA signature from contributor."""
        comment = f"""
        Thank you for your contribution! Before we can merge this PR,
        we need you to sign our Contributor License Agreement (CLA).
        
        Please sign the CLA at: [CLA Signing URL]
        
        Once signed, this check will automatically pass.
        """
        
        # Post comment on PR
        # Set CLA check status to pending
    
    def approve_cla_check(self, pr_data: Dict) -> None:
        """Approve CLA check for contributor."""
        # Set CLA check status to success
        # Post approval comment if needed
```

### Maintenance and Updates

#### Version Updates

```python
def update_cla_version(new_version: str, new_text: str) -> None:
    """Update CLA to new version."""
    cla_manager = CLAManager('signatures/version1/cla.json')
    
    # Update version
    cla_manager.cla_data['version'] = new_version
    cla_manager.cla_data['agreement_text'] = new_text
    cla_manager.cla_data['update_date'] = datetime.now().isoformat()
    
    # Save changes
    cla_manager.save_cla_data()
    
    # Notify existing contributors of update
    notify_contributors_of_update(new_version)

def migrate_contributors_to_new_version(new_version: str) -> None:
    """Migrate contributors to new CLA version."""
    # Send notifications
    # Track re-signatures
    # Update contributor records
    pass
```

#### Compliance Monitoring

```python
def generate_compliance_report() -> Dict:
    """Generate comprehensive compliance report."""
    cla_manager = CLAManager('signatures/version1/cla.json')
    
    return {
        "cla_compliance": cla_manager.generate_cla_report(),
        "license_compatibility": check_all_licenses(),
        "signature_validity": validate_all_signatures(),
        "recent_activity": get_recent_compliance_activity()
    }

def audit_contributor_compliance() -> List[Dict]:
    """Audit all contributor compliance."""
    # Check all contributors
    # Validate signatures
    # Identify compliance issues
    # Return audit results
    pass
```

### Best Practices Summary

1. **CLA Management**: Maintain accurate and up-to-date CLA records
2. **Automation**: Automate CLA checking in CI/CD pipelines
3. **Legal Compliance**: Ensure all contributions comply with licensing terms
4. **Version Control**: Track CLA versions and maintain backward compatibility
5. **Documentation**: Keep clear records of all legal agreements and signatures