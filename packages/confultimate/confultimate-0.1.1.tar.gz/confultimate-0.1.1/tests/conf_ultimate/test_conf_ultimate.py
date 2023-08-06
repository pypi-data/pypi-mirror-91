import pytest
import os

from confultimate.conf_ultimate import ConfUltimate

def test_not_existing_path():
    """Test to check an unexiting path"""
    
    with pytest.raises(FileNotFoundError):
        ConfUltimate.load(["/null"])
    ConfUltimate.clean()
    
def test_empty_conf():
    """Test to check an unexiting path"""
    with pytest.raises(Exception):
        ConfUltimate.load([])
    
def test_multiple_file(resource_path):
    """Test to check an unexiting path"""
    file1 = os.path.join(resource_path, "conf1.json")
    file2 = os.path.join(resource_path, "conf2.json")
    
    ConfUltimate.load([file1, file2])

    assert ConfUltimate.getInstance().getConfig()["conf1"] == "test"
    assert ConfUltimate.getInstance().getConfig()["conf2"] == "test"
    assert ConfUltimate.getInstance().getConfig()["conf_commun"] == "conf2"
    assert ConfUltimate.getInstance().getConfig()["conf_commun_list"] == ["conf2"]
    ConfUltimate.clean()
    
    with pytest.raises(Exception):
        ConfUltimate.getConfig()
    


