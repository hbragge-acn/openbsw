import pytest

@pytest.mark.parametrize("block_id,value", [
    ("2561", "aabb"),
    ("2817", "01ff"),
])
def test_storage_write_and_read(target_session, block_id, value):
    capserial = target_session.capserial()
    assert capserial.wait_for_boot_complete()

    # Write command
    write_command = f"storage write {block_id} {value}\n"
    write_expected = [
        b"Writing ok",
        b"ok",
        f'Received console command "storage write {block_id} {value}"'.encode(),
        b"Console command succeeded",
    ]
    capserial.clear()
    capserial.send_command(write_command.encode())
    success, output, _ = capserial.read_until(write_expected, timeout=2, match_all_expected=True)
    assert success, f"Write failed for block_id={block_id}, value={value}"

    # Reset the device
    target_session.restart()
    assert capserial.wait_for_boot_complete()

    # Read command
    read_command = f"storage read {block_id} {len(value)//2}\n"
    read_expected = [
        b"Reading ok",
        b"ok",
        f'Received console command "storage read {block_id} {len(value)//2}"'.encode(),
        b"Console command succeeded",
    ]
    capserial.clear()
    capserial.send_command(read_command.encode())
    success, output, _ = capserial.read_until(read_expected, timeout=2, match_all_expected=True)
    assert success, f"Read failed for block_id={block_id}"

    # Check that the returned data matches what was written
    # The output should contain the bytes in hex, e.g., "0    : 01ff"
    expected_line = f"0    : {value}"
    found = any(expected_line.encode() in line for line in output)
    assert found, f"Expected line '{expected_line}' not found in output: {output}"

@pytest.mark.parametrize("block_id,fill_value,fill_size", [
    ("2561", "ab", 4),
    ("2817", "01", 2),
])
def test_storage_fill_and_read(target_session, block_id, fill_value, fill_size):
    capserial = target_session.capserial()
    assert capserial.wait_for_boot_complete()

    # Fill command
    fill_command = f"storage fill {block_id} 0x{fill_value} {fill_size}\n"
    fill_expected = [
        b"Fill ok",
        b"ok",
        f'Received console command "storage fill {block_id} 0x{fill_value} {fill_size}"'.encode(),
        b"Console command succeeded",
    ]
    capserial.clear()
    capserial.send_command(fill_command.encode())
    success, output, _ = capserial.read_until(fill_expected, timeout=2, match_all_expected=True)
    assert success, f"Fill failed for block_id={block_id}, value={fill_value}, size={fill_size}"

    # Reset the device
    target_session.restart()
    assert capserial.wait_for_boot_complete()

    # Read command to verify fill
    read_command = f"storage read {block_id} {fill_size}\n"
    read_expected = [
        b"Reading ok",
        b"ok",
        f'Received console command "storage read {block_id} {fill_size}"'.encode(),
        b"Console command succeeded",
    ]
    capserial.clear()
    capserial.send_command(read_command.encode())
    success, output, _ = capserial.read_until(read_expected, timeout=2, match_all_expected=True)
    assert success, f"Read after fill failed for block_id={block_id}"

    # Check that the returned data matches the fill value
    expected_filled = fill_value * fill_size
    expected_line = f"0    : {expected_filled}"
    found = any(expected_line.encode() in line for line in output)
    assert found, f"Expected filled line '{expected_line}' not found in output: {output}"