"""
Prompt Loader Module
Load and manage YAML prompt templates.
"""

import os
import yaml
from typing import Dict, Optional
from pathlib import Path


class PromptLibrary:
    """Manage and load prompt templates from YAML files."""
    
    def __init__(self, prompts_dir: Optional[str] = None):
        """
        Initialize prompt library.
        
        Args:
            prompts_dir: Directory containing YAML prompt files
        """
        if prompts_dir is None:
            # Default to current directory's prompts folder
            prompts_dir = Path(__file__).parent
        
        self.prompts_dir = Path(prompts_dir)
        self.prompts = {}
        self._load_all_prompts()
    
    def _load_all_prompts(self):
        """Load all YAML prompt files from directory."""
        
        yaml_files = [
            'system_prompts.yaml',
            'query_prompts.yaml',
            'summarization_prompts.yaml',
            'compare_docs_prompts.yaml'
        ]
        
        for yaml_file in yaml_files:
            file_path = self.prompts_dir / yaml_file
            if file_path.exists():
                category = yaml_file.replace('.yaml', '').replace('_', '.')
                self.prompts[category] = self._load_yaml(file_path)
    
    def _load_yaml(self, file_path: Path) -> Dict:
        """Load a single YAML file."""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not load {file_path}: {e}")
            return {}
    
    def get_prompt(self, category: str, name: str) -> Optional[Dict]:
        """
        Get a specific prompt by category and name.
        
        Args:
            category: Prompt category (e.g., 'system_prompts', 'query_prompts')
            name: Prompt name within category
            
        Returns:
            Prompt dictionary or None
        """
        category_key = category.replace('_', '.')
        return self.prompts.get(category_key, {}).get(name)
    
    def get_template(self, category: str, name: str) -> Optional[str]:
        """
        Get just the template string from a prompt.
        
        Args:
            category: Prompt category
            name: Prompt name
            
        Returns:
            Template string or None
        """
        prompt = self.get_prompt(category, name)
        if prompt:
            return prompt.get('template') or prompt.get('content')
        return None
    
    def render_template(
        self,
        category: str,
        name: str,
        variables: Dict
    ) -> Optional[str]:
        """
        Render a prompt template with variables.
        
        Args:
            category: Prompt category
            name: Prompt name
            variables: Dictionary of variables to substitute
            
        Returns:
            Rendered prompt string
        """
        template = self.get_template(category, name)
        if not template:
            return None
        
        # Simple variable substitution
        rendered = template
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            rendered = rendered.replace(placeholder, str(value))
        
        return rendered
    
    def list_prompts(self, category: Optional[str] = None) -> Dict:
        """
        List available prompts.
        
        Args:
            category: Optional category filter
            
        Returns:
            Dictionary of available prompts
        """
        if category:
            category_key = category.replace('_', '.')
            return {category_key: list(self.prompts.get(category_key, {}).keys())}
        
        return {cat: list(prompts.keys()) for cat, prompts in self.prompts.items()}
    
    def get_system_prompt(self, role: str = 'document_assistant') -> str:
        """
        Get a system prompt by role.
        
        Args:
            role: System role name
            
        Returns:
            System prompt content
        """
        prompt = self.get_prompt('system.prompts', role)
        if prompt:
            return prompt.get('content', '')
        return ''
    
    def get_query_template(self, query_type: str = 'basic_qa') -> str:
        """
        Get a query template by type.
        
        Args:
            query_type: Query template type
            
        Returns:
            Query template string
        """
        return self.get_template('query.prompts', query_type) or ''


# Global instance
_prompt_library = None


def get_prompt_library() -> PromptLibrary:
    """Get or create global prompt library instance."""
    global _prompt_library
    if _prompt_library is None:
        _prompt_library = PromptLibrary()
    return _prompt_library


# Convenience functions
def get_prompt(category: str, name: str) -> Optional[Dict]:
    """Get a prompt from the global library."""
    return get_prompt_library().get_prompt(category, name)


def render_prompt(category: str, name: str, **variables) -> Optional[str]:
    """Render a prompt template from the global library."""
    return get_prompt_library().render_template(category, name, variables)


def get_system_prompt(role: str = 'document_assistant') -> str:
    """Get a system prompt from the global library."""
    return get_prompt_library().get_system_prompt(role)


def get_query_template(query_type: str = 'basic_qa') -> str:
    """Get a query template from the global library."""
    return get_prompt_library().get_query_template(query_type)
