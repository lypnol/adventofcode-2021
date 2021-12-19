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
        total = packet_version
        if packet_type_id == 4:
            # literal
            j = 6
            while packet[j] == "1":
                j += 5
            return total, j + 5
        else:
            length_type_id = packet[6]
            if length_type_id == "0":
                length = int(packet[7:22], 2)
                j = 22
                while j < 22 + length:
                    subpacket = packet[j:]
                    val, jj = self.parse_packet(subpacket)
                    j += jj
                    total += val
            else:
                nb_subpackets = int(packet[7:18], 2)
                j = 18
                nb_parsed_subpackets = 0
                while nb_parsed_subpackets < nb_subpackets:
                    subpacket = packet[j:]
                    val, jj = self.parse_packet(subpacket)
                    j += jj
                    nb_parsed_subpackets += 1
                    total += val

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
    D2FE28
    """.strip()
        )
        == 6
    )
    assert (
        ThChSubmission().run(
            """
    8A004A801A8002F478
    """.strip()
        )
        == 16
    )
    assert (
        ThChSubmission().run(
            """
    620080001611562C8802118E34
    """.strip()
        )
        == 12
    )
    assert (
        ThChSubmission().run(
            """
    C0015000016115A2E0802F182340
    """.strip()
        )
        == 23
    )
    assert (
        ThChSubmission().run(
            """
    A0016C880162017C3686B18A3D4780
    """.strip()
        )
        == 31
    )
