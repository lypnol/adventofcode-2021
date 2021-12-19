from tool.runners.python import SubmissionPy


class ThChSubmission(SubmissionPy):
    def hex_to_binary(self, hexa):
        binary = []
        for hex_char in hexa:
            binary_char = bin(int(hex_char, 16))[2:]
            binary.append(binary_char.zfill(4))
        return "".join(binary)

    def parse_header(self, packet):
        packet_version = int(packet[:3], 2)
        packet_type_id = int(packet[3:6], 2)
        return packet_version, packet_type_id

    def parse_packet(self, packet):
        packet_version, packet_type_id = self.parse_header(packet)
        if packet_type_id == 4:
            # literal
            bits = []
            j = 6
            while True:
                bits.append(packet[j + 1 : j + 5])
                is_last = packet[j] == "0"
                j += 5
                if is_last:
                    break
            return int("".join(bits), 2), j
        else:
            length_type_id = packet[6]
            values = []
            if length_type_id == "0":
                length = int(packet[7:22], 2)
                j = 22
                while j < 22 + length:
                    subpacket = packet[j:]
                    val, jj = self.parse_packet(subpacket)
                    j += jj
                    values.append(val)
            else:
                nb_subpackets = int(packet[7:18], 2)
                j = 18
                nb_parsed_subpackets = 0
                while nb_parsed_subpackets < nb_subpackets:
                    subpacket = packet[j:]
                    val, jj = self.parse_packet(subpacket)
                    j += jj
                    nb_parsed_subpackets += 1
                    values.append(val)

            if packet_type_id == 0:
                total = sum(values)
            elif packet_type_id == 1:
                total = 1
                for val in values:
                    total = total * val
            elif packet_type_id == 2:
                total = min(values)
            elif packet_type_id == 3:
                total = max(values)
            elif packet_type_id == 5:
                total = 1 if values[0] > values[1] else 0
            elif packet_type_id == 6:
                total = 1 if values[0] < values[1] else 0
            elif packet_type_id == 7:
                total = 1 if values[0] == values[1] else 0

            return total, j

    def run(self, s):
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        packet = self.hex_to_binary(s)
        total, _ = self.parse_packet(packet)
        return total


def test_th_ch():
    """
    Run `python -m pytest ./day-16/part-1/th-ch.py` to test the submission.
    """
    assert (
        ThChSubmission().run(
            """
    C200B40A82
    """.strip()
        )
        == 3
    )
    assert (
        ThChSubmission().run(
            """
    04005AC33890
    """.strip()
        )
        == 54
    )
    assert (
        ThChSubmission().run(
            """
    880086C3E88112
    """.strip()
        )
        == 7
    )
    assert (
        ThChSubmission().run(
            """
    CE00C43D881120
    """.strip()
        )
        == 9
    )
    assert (
        ThChSubmission().run(
            """
    D8005AC2A8F0
    """.strip()
        )
        == 1
    )
    assert (
        ThChSubmission().run(
            """
    F600BC2D8F
    """.strip()
        )
        == 0
    )
    assert (
        ThChSubmission().run(
            """
    9C005AC2F8F0
    """.strip()
        )
        == 0
    )
    assert (
        ThChSubmission().run(
            """
    9C0141080250320F1802104A08
    """.strip()
        )
        == 1
    )
