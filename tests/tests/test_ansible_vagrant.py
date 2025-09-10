import os


def test_vagrant_run(collection_path, vagrant_run):
    host = vagrant_run(
        playbook=os.path.join(collection_path, "tests", "playbook-vms.yaml"),
        project_dir=collection_path,
    )

    assert host.file("/etc/testfile").is_file
