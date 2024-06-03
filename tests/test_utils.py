import os
import pytest
from unittest.mock import MagicMock, patch
from burparse.utils import readConfig, getReportDict, saveCSVFile, getFileType

@pytest.fixture
def sample_issue():
    issue = MagicMock()
    issue.find.return_value = MagicMock()
    issue.find('name').text = "Sample Issue"
    issue.find('host').attrib = {"ip": "127.0.0.1"}
    issue.find('host').text = "localhost"
    issue.find('path').text = "/path/to/issue"
    issue.find('location').text = "Location of issue"
    issue.find('severity').text = "High"
    issue.find('confidence').text = "High"
    issue.find('issueBackground').text = "<p>Background</p>"
    issue.find('remediationBackground').text = "<p>Remediation</p>"
    issue.find('vulnerabilityClassification').text = "<ul>Classification</ul>"
    issue.find('requestresponse').find('request').text = "dGVzdCBxdWVzdGlvbg=="
    issue.find('requestresponse').find('response').text = "dGVzdCBwYXNzd29yZA=="
    issue.find('issueDetail').text = "Detail of issue"
    return issue

def test_readConfig(tmp_path):
    config_file = tmp_path / "SORT.conf"
    with open(config_file, 'w') as f:
        f.write("# This is a comment\n\nname\nhost\nip\n")

    assert readConfig(config_file) == ['name', 'host', 'ip']

@pytest.mark.skip(reason="Borked")
def test_getReportDict(sample_issue):
    arguments = MagicMock(verbose=False)
    report_dict = getReportDict(sample_issue, arguments)

    assert report_dict['name'] == "Sample Issue"
    assert report_dict['host'] == "localhost"
    assert report_dict['ip'] == "127.0.0.1"
    assert report_dict['path'] == "/path/to/issue"
    assert report_dict['location'] == "Location of issue"
    assert report_dict['severity'] == "High"
    assert report_dict['confidence'] == "High"
    assert report_dict['issueBackground'] == "Background"
    assert report_dict['remediationBackground'] == "Remediation"
    assert report_dict['vulnerabilityClassification'] == "Classification"
    assert report_dict['request'] == b'test question'
    assert report_dict['response'] == b'test password'
    assert report_dict['issueDetail'] == "Detail of issue"

@patch('burparse.utils.DictWriter')
def test_saveCSVFile(mock_DictWriter, tmp_path):
    reports = [
        {'name': 'Sample Issue 1', 'host': 'localhost', 'severity': 'High'},
        {'name': 'Sample Issue 2', 'host': 'localhost', 'severity': 'Medium'}
    ]
    file_path = tmp_path / "output.csv"
    args = MagicMock(Force=False, verbose=False, Slow=False)

    saveCSVFile(reports, file_path, args)

    assert mock_DictWriter.return_value.writeheader.called
    assert mock_DictWriter.return_value.writerow.call_count == 2
    assert os.path.exists(file_path)

def test_getFileType(tmp_path):
    files = [
        str(tmp_path / "file1.xml"),
        str(tmp_path / "file2.txt"),
        str(tmp_path / "file3.xml")
    ]
    args = MagicMock(verbose=True)

    result = getFileType(files, ".xml", args)

    assert len(result) == 2
    assert result == [files[0], files[2]]
