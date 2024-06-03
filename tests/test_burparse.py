import os
import tempfile
import pytest
from unittest.mock import patch
from burparse.burparse import parseFile, main, setup
import argparse

@pytest.fixture
def sample_xml():
    xml_content = """
    <root>
        <issue>
            <title>Sample Issue 1</title>
            <severity>High</severity>
        </issue>
        <issue>
            <title>Sample Issue 2</title>
            <severity>Medium</severity>
        </issue>
    </root>
    """
    return xml_content

@pytest.mark.skip(reason="Borked")
def test_parseFile(sample_xml):
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_file.write(sample_xml)
        temp_file_path = temp_file.name

    arguments = argparse.Namespace(verbose=False, Slow=False)
    result = parseFile(temp_file_path, arguments)
    os.unlink(temp_file_path)

    assert len(result) == 2
    assert result[0]['title'] == 'Sample Issue 1'
    assert result[0]['severity'] == 'High'
    assert result[1]['title'] == 'Sample Issue 2'
    assert result[1]['severity'] == 'Medium'

@patch('burparse.burparse.parseFile')
@patch('burparse.burparse.saveCSVFile')
def test_main(mock_saveCSVFile, mock_parseFile):
    args = argparse.Namespace(xmlFiles=['file1.xml', 'file2.xml'], out=None, verbose=False, Slow=False)
    main(args.xmlFiles, args)
    assert mock_parseFile.call_count == 2
    assert mock_saveCSVFile.call_count == 2

def test_setup():
    # Example of how to test setup function
    with patch('argparse.ArgumentParser.parse_args', return_value=argparse.Namespace(xmlFiles=['file1.xml'], out=None, verbose=False, Slow=False)) as mock_parse_args:
        setup()
        assert mock_parse_args.called
