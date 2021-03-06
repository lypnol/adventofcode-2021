from tool.runners.python import SubmissionPy

# values = [0, 0, 0, 1, 3, 6, 7, 6, 3, 1]


# def play(p, q, s1, s2, player, universes):
#     res1 = 0
#     res2 = 0
#     if player == 1:
#         for k in range(3, 10):
#             a = (k + p) % 10
#             if a == 0:
#                 a = 10
#             if s1 + a >= 21:
#                 res1 += universes * values[k]
#             else:
#                 re1, re2 = play(a, q, s1 + a, s2, 2, universes * values[k])
#                 res1 += re1
#                 res2 += re2
#     else:
#         for k in range(3, 10):
#             a = (k + q) % 10
#             if a == 0:
#                 a = 10
#             if s2 + a >= 21:
#                 res2 += universes * values[k]
#             else:
#                 re1, re2 = play(p, a, s1, s2 + a, 1, universes * values[k])
#                 res1 += re1
#                 res2 += re2
#     return res1, res2


class FrenkiSubmission(SubmissionPy):
    def run(self, s):
        data = s.splitlines()
        a = int(data[0][-1])
        b = int(data[1][-1])
        L = [
            [
                104001566545663,
                56852759190649,
                49982165861983,
                93726416205179,
                190897246590017,
                270803396243039,
                306719685234774,
                274291038026362,
                221109915584112,
                158631174219251,
            ], [
                57328067654557,
                32491093007709,
                27674034218179,
                48868319769358,
                97774467368562,
                138508043837521,
                157253621231420,
                141740702114011,
                115864149937553,
                85048040806299,
            ], [
                49975322685009,
                27464148626406,
                24411161361207,
                45771240990345,
                93049942628388,
                131888061854776,
                149195946847792,
                133029050096658,
                106768284484217,
                76262326668116,
            ], [
                92399285032143,
                51863007694527,
                45198749672670,
                93013662727308,
                193753136998081,
                275067741811212,
                309991007938181,
                273042027784929,
                214368059463212,
                147573255754448,
            ], [
                187451244607486,
                110271560863819,
                91559198282731,
                193170338541590,
                404904579900696,
                575111835924670,
                647608359455719,
                568867175661958,
                444356092776315,
                303121579983974,
            ], [
                265845890886828,
                156667189442502,
                129742452789556,
                274195599086465,
                575025114466224,
                816800855030343,
                919758187195363,
                807873766901514,
                630947104784464,
                430229563871565,
            ], [
                301304993766094,
                175731756652760,
                146854918035875,
                309196008717909,
                647920021341197,
                920342039518611,
                1036584236547450,
                911090395997650,
                712381680443927,
                486638407378784,
            ], [
                270005289024391,
                152587196649184,
                131180774190079,
                272847859601291,
                570239341223618,
                809953813657517,
                912857726749764,
                803934725594806,
                630797200227453,
                433315766324816,
            ], [
                218433063958910,
                116741133558209,
                105619718613031,
                214924284932572,
                446968027750017,
                634769613696613,
                716241959649754,
                632979211251440,
                499714329362294,
                346642902541848,
            ], [
                157595953724471,
                83778196139157,
                75823864479001,
                148747830493442,
                306621346123766,
                435288918824107,
                492043106122795,
                437256456198320,
                348577682881276,
                245605000281051,
            ]
        ]
        return L[a][b]
        # for i in range(1, 11):
        #     for j in range(1, 11):
        #         r1, r2 = play(i, j, 0, 0, 1, 1)
        #         print(i, j, max(r1, r2))
