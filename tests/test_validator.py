"""
Basic tests for the docx-validator package.
"""


import pytest

from docx_validator import DocxValidator, ValidationResult, ValidationSpec
from docx_validator.parser import DocxParser


def test_validation_spec_creation():
    """Test creating a ValidationSpec."""
    spec = ValidationSpec(
        name="Test Spec",
        description="This is a test specification",
        category="test"
    )
    assert spec.name == "Test Spec"
    assert spec.description == "This is a test specification"
    assert spec.category == "test"


def test_validation_result_creation():
    """Test creating a ValidationResult."""
    result = ValidationResult(
        spec_name="Test Spec",
        passed=True,
        confidence=0.95,
        reasoning="Document meets all requirements"
    )
    assert result.spec_name == "Test Spec"
    assert result.passed is True
    assert result.confidence == 0.95
    assert result.reasoning == "Document meets all requirements"


def test_docx_parser_file_not_found():
    """Test that DocxParser raises FileNotFoundError for missing files."""
    parser = DocxParser()
    with pytest.raises(FileNotFoundError):
        parser.parse_docx("nonexistent_file.docx")


def test_docx_parser_invalid_extension():
    """Test that DocxParser raises ValueError for non-.docx files."""
    import os
    import tempfile

    parser = DocxParser()

    # Create a temporary file with wrong extension
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("test")
        temp_path = f.name

    try:
        with pytest.raises(ValueError, match="must be a .docx file"):
            parser.parse_docx(temp_path)
    finally:
        os.unlink(temp_path)


def test_validation_spec_from_json():
    """Test loading ValidationSpec from JSON."""
    json_data = {
        "name": "Has Title",
        "description": "Document must have a title",
        "category": "metadata"
    }
    spec = ValidationSpec(**json_data)
    assert spec.name == "Has Title"
    assert spec.description == "Document must have a title"
    assert spec.category == "metadata"


def test_validator_initialization():
    """Test DocxValidator initialization."""
    import os

    # Set a test API key for initialization
    os.environ["OPENAI_API_KEY"] = "test_key"

    try:
        # Test default OpenAI backend
        validator = DocxValidator(
            model_name="gpt-4o-mini",
            api_key="test_key",
        )
        assert validator.backend.name == "openai"

        # Test GitHub backend
        validator_github = DocxValidator(
            backend="github",
            model_name="gpt-4o-mini",
            api_key="test_key",
        )
        assert validator_github.backend.name == "openai"  # GitHub uses OpenAI backend

        # Test NebulaOne backend
        validator_nebula = DocxValidator(
            backend="nebulaone",
            model_name="nebula-1",
            api_key="test_key",
        )
        assert validator_nebula.backend.name == "nebulaone"
    finally:
        # Clean up
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]


def test_backend_registry():
    """Test that all backends are registered correctly."""
    from docx_validator.backends import BACKENDS

    assert "openai" in BACKENDS
    assert "github" in BACKENDS
    assert "nebulaone" in BACKENDS


def test_get_backend():
    """Test the get_backend function."""
    import os

    from docx_validator.backends import get_backend

    os.environ["OPENAI_API_KEY"] = "test_key"

    try:
        # Test creating backends
        openai_backend = get_backend("openai", model_name="gpt-4")
        assert openai_backend.name == "openai"

        nebula_backend = get_backend("nebulaone", model_name="nebula-1")
        assert nebula_backend.name == "nebulaone"

        # Test invalid backend
        try:
            get_backend("invalid_backend")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Unknown backend" in str(e)
    finally:
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
