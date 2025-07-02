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

    #TODO: can be uncommented once driver changes are in
    # Check that the returned data matches what was written
    # The output should contain the bytes in hex, e.g., "0: 0xaa", "1: 0xbb"
    # expected_bytes = [f"0x{value[i:i+2]}" for i in range(0, len(value), 2)]
    # for block_idx, byte in enumerate(expected_bytes):
    #     assert f"{block_idx}: {byte}".encode() in output, f"Byte {byte} not found in output"
