import random


def get_payoffs(my_move: str, opponent_move: str) -> tuple[int, int]:
    if my_move == "C" and opponent_move == "C":
        return (3, 3)
    elif my_move == "C" and opponent_move == "D":
        return (0, 5)
    elif my_move == "D" and opponent_move == "C":
        return (5, 0)
    elif my_move == "D" and opponent_move == "D":
        return (1, 1)
    else:
        raise ValueError("get_payoffs: invalid arguments")
    
# ALL STRATEGIES HERE

def always_cooperate(my_moves: list[str], opponent_moves: list[str]) -> str:
    return "C"


def always_defect(my_moves: list[str], opponent_moves: list[str]) -> str:
    return "D"


def tit_for_tat(my_moves: list[str], opponent_moves: list[str]) -> str:
    if not opponent_moves:
        return "C"
    return opponent_moves[-1]


def suspicious_tit_for_tat(my_moves: list[str], opponent_moves: list[str]) -> str:
    if not opponent_moves:
        return "D"
    return opponent_moves[-1]


def six_seven_for_tat(my_moves: list[str], opponent_moves: list[str]) -> str:
    if not opponent_moves:
        return "C"
    if len(my_moves) == 67:
        return "D"
    return opponent_moves[-1]


def hater(my_moves: list[str], opponent_moves: list[str]) -> str:
    if len(opponent_moves) < 2:
        return "D"
    if opponent_moves[-2] == "C":
        return "C"
    else:
        return "D"


#def joss(my_moves: list[str], opponent_moves: list[str]) -> str:
    if not opponent_moves or opponent_moves[-1] == "C":
        if random.random() < 0.1:
            return "D"
        return "C"
    return "D"


#def soft_majority(my_moves: list[str], opponent_moves: list[str]) -> str:
    if opponent_moves.count("C") >= opponent_moves.count("D"):
        return "C"
    return "D"


#def gradual(my_moves: list[str], opponent_moves: list[str]) -> str:
    planned: list[str] = []
    defections = 0
    for move in opponent_moves:
        if planned:
            planned.pop(0)
        if move == "D":
            defections += 1
            if not planned:
                planned = ["D"] * defections + ["C", "C"]
    if planned:
        return planned[0]
    return "C"


def grudger(my_moves: list[str], opponent_moves: list[str]) -> str:
    if "D" in opponent_moves:
        return "D"
    else:
        return "C"


def contrarian(my_moves: list[str], opponent_moves: list[str]) -> str:
    if not opponent_moves:
        return "D"
    if opponent_moves[-1] == "C":
        return "D"
    else:
        return "C"


def slow_tit_for_tat(my_moves: list[str], opponent_moves: list[str]) -> str:
    if len(opponent_moves) < 2:
        return "C"
    return opponent_moves[-2]


def random_strat(my_moves: list[str], opponent_moves: list[str]) -> str:
    choice = random.randint(0,1)
    if choice == 1:
        return "C"
    else:
        return "D"


def emotional(my_moves: list[str], opponent_moves: list[str]) -> str:
    if not opponent_moves:
        return "C"
    payoffs = get_payoffs(my_moves[-1], opponent_moves[-1])
    if payoffs[0] > payoffs[1]:
        return "C"
    elif payoffs[0] == payoffs[1]:
        return my_moves[-1]
    else:
        return "D"


def indecisive(my_moves: list[str], opponent_moves: list[str]) -> str:
    if not opponent_moves:
        return "C"
    if my_moves[-1] == "C":
        return "D"
    else:
        return "C"


def opus(my_moves: list[str], opponent_moves: list[str]) -> str:
    n = len(opponent_moves)
    if n == 0:
        return "C"

    # 1. Opponent that almost always defects: stop feeding it points.
    if n >= 20:
        recent = opponent_moves[-20:]
        if recent.count("D") >= 17 and opponent_moves[-3:].count("C") < 2:
            return "D"

    # 2. Opponent that ignores what I do (random or noise-like): defect.
    if n >= 40:
        after_c = after_c_coop = after_d = after_d_coop = 0
        for i in range(1, n):
            if my_moves[i - 1] == "C":
                after_c += 1
                after_c_coop += opponent_moves[i] == "C"
            else:
                after_d += 1
                after_d_coop += opponent_moves[i] == "C"
        if after_c >= 10 and after_d >= 10:
            responsiveness = after_c_coop / after_c - after_d_coop / after_d
            coop_rate = opponent_moves[-40:].count("C") / 40
            if abs(responsiveness) < 0.15 and 0.25 < coop_rate < 0.75:
                return "D"

    # 3. Tit-for-tat core: reward cooperation.
    if opponent_moves[-1] == "C":
        return "C"

    # 4. Opponent defected. Sometimes forgive, to break retaliation loops.
    last_forgive = -100
    for i in range(n - 1, 0, -1):
        if my_moves[i] == "C" and opponent_moves[i - 1] == "D":
            last_forgive = i
            break

    if n >= 2 and n - last_forgive > 8:
        overall_coop = opponent_moves.count("C") / n
        mutual_d_streak = (my_moves[-1] == "D" and my_moves[-2] == "D"
                           and opponent_moves[-2] == "D")
        echo = (my_moves[-2] == "D" and opponent_moves[-2] == "C"
                and my_moves[-1] == "C")
        if overall_coop > 0.6 and (mutual_d_streak or echo):
            return "C"

    return "D"


def sonnet(my_moves, opponent_moves):
    n = len(my_moves)
    if n == 0:
        return "C"
    opp = opponent_moves
    total = n
    opp_d = opp.count("D")

    # Endgame: defect on the final rounds (unknown length ~500, so only very late)
    # Skipped to avoid hurting cooperation if the length is shorter than expected.

    # Always-defect opponent: stop being exploited
    if n >= 10 and opp_d == n:
        return "D"

    # Random/mostly-defecting opponent: defect
    if n >= 30 and opp_d / total > 0.6:
        return "D"

    # Detect unconditional cooperators (never retaliates against my defections)
    # Test: if I defected several times and they still cooperated every time after
    if n >= 20:
        my_d_idx = [i for i in range(n - 1) if my_moves[i] == "D"]
        if len(my_d_idx) >= 3 and opp_d == 0:
            return "D"

    # Detect Alternator-style / always-cooperate exploitation only when safe:
    # periodic probe is avoided to keep cooperation stable.

    # Handling opponent's last move
    last = opp[-1]
    prev = opp[-2] if n >= 2 else "C"

    # Forgiving tit-for-two-tats core
    if last == "D" and prev == "D":
        return "D"

    # Retaliate on a single defection only if the opponent defects often
    if last == "D":
        if opp_d / total > 0.25:
            return "D"
        return "C"

    # Break mutual defection spirals: if both defected last 3 rounds, try to cooperate
    if n >= 3 and my_moves[-3:] == ["D"] * 3 and opp[-3:] == ["D"] * 3:
        return "C"

    return "C"


def haiku(my_moves: list[str], opponent_moves: list[str]) -> str:
    # Opening move: cooperate
    if not opponent_moves:
        return "C"

    n = len(opponent_moves)

    # Unconditional defector: after 20 rounds with no cooperation, defect too
    if n >= 20 and "C" not in opponent_moves:
        return "D"

    # Break mutual-defection loops with a cooperative probe
    if n >= 2 and my_moves[-1] == "D" and my_moves[-2] == "D" \
            and opponent_moves[-1] == "D" and opponent_moves[-2] == "D":
        return "C"

    # Otherwise mirror the opponent's last move
    return opponent_moves[-1]


def hydrogen(my_moves: list[str], opponent_moves: list[str]) -> str:
    n = len(my_moves)
    if n == 0:
        return "C"

    opp_c_total = opponent_moves.count("C")
    opp_c_rate = opp_c_total / n

    # Lock down against pure defectors (e.g., AllD)
    if n >= 6 and opp_c_total == 0:
        return "D"

    # Exploit random or unresponsive bots whose moves don't depend on ours
    if n >= 24:
        c_after_c, total_after_c = 0, 0
        c_after_d, total_after_d = 0, 0
        for i in range(n - 1):
            if my_moves[i] == "C":
                total_after_c += 1
                if opponent_moves[i + 1] == "C":
                    c_after_c += 1
            else:
                total_after_d += 1
                if opponent_moves[i + 1] == "C":
                    c_after_d += 1

        if total_after_c >= 6 and total_after_d >= 6:
            rate_c = c_after_c / total_after_c
            rate_d = c_after_d / total_after_d
            if abs(rate_c - rate_d) < 0.12 and 0.15 <= opp_c_rate <= 0.85:
                return "D"

    # Break alternating retaliation loops (CD/DC echo spirals)
    if n >= 6:
        if (
            my_moves[-4:] == ["C", "D", "C", "D"]
            and opponent_moves[-4:] == ["D", "C", "D", "C"]
        ) or (
            my_moves[-4:] == ["D", "C", "D", "C"]
            and opponent_moves[-4:] == ["C", "D", "C", "D"]
        ):
            return "C"

    # Break mutual defection deadlocks periodically if opponent has shown willingness to cooperate
    if n >= 8 and my_moves[-6:] == ["D"] * 6 and opponent_moves[-6:] == ["D"] * 6:
        if opp_c_rate > 0.20 and n % 23 == 0:
            return "C"
        return "D"

    # Standard Tit-for-Tat reciprocity with measured forgiveness for isolated noise/probes
    if opponent_moves[-1] == "C":
        return "C"

    # Forgive a single isolated defection if the opponent has been overwhelmingly cooperative
    if (
        n >= 10
        and opp_c_rate >= 0.88
        and opponent_moves[-4:-1] == ["C", "C", "C"]
        and my_moves[-4:] == ["C", "C", "C", "C"]
    ):
        return "C"

    return "D"


def luna(my_moves: list[str], opponent_moves: list[str]) -> str:
    n = len(opponent_moves)
    if n == 0:
        return "C"
    recent = opponent_moves[-12:]
    if recent.count("D") >= 3:
        return "D"
    if len(recent) >= 4 and all(move == "C" for move in recent[-4:]):
        return "C"

    if opponent_moves[-1] == "D":
        return "D"
    return "C"


def v4flash(my_moves: list[str], opponent_moves: list[str]) -> str:
    if not opponent_moves:
        return "C"
    if opponent_moves[-1] == "D":
        if len(opponent_moves) >= 2 and opponent_moves[-2] == "D" and my_moves[-1] == "D":
            return "C"
        return "D"
    return "C"


def grok(my_moves: list[str], opponent_moves: list[str]) -> str:
    n = len(opponent_moves)
    if n == 0:
        return "C"
    opp = opponent_moves
    me = my_moves
    if n >= 10 and opp[-10:].count("D") >= 8:
        return "D"
    if (
        n >= 23
        and me[18] == "D"
        and me[19] == "C"
        and me[20] == "D"
        and me[21] == "D"
        and opp[19] == "C"
        and opp[22] == "D"
    ):
        return "C" if me[-1] == "D" else "D"
    d = opp.count("D")
    if d == 0:
        if n == 18:
            return "D"
        if n == 19:
            return "C"
        if n >= 20 and me[18] == "D" and opp[19] == "C":
            if n <= 21:
                return "D"
            if n == 22:
                return "C"
            return "D"
        return "C"
    if n >= 21 and me[18] == "D" and opp[19] == "D" and opp[20] == "D" and "C" not in opp[20:]:
        return "D"
    if n == 20 and me[18] == "D" and opp[19] == "D":
        return "C"
    if me.count("D") >= 2:
        ignored = punished = 0
        for i in range(n - 1):
            if me[i] == "D":
                if opp[i + 1] == "C":
                    ignored += 1
                else:
                    punished += 1
        if punished == 0 and ignored >= 2:
            return "D"
    if opp[-1] == "C":
        return "C"
    if me[-1] == "C":
        return "D"
    if d <= 3 and (n - d) > d:
        return "C"
    return "D"


strategies: dict[str, function] = {
    "Always Cooperate": always_cooperate,
    "Always Defect": always_defect,
    "Tit for Tat": tit_for_tat,
    "Suspicious Tit for Tat": suspicious_tit_for_tat,
    "Six Seven for Tat": six_seven_for_tat,
    "Hater": hater,
    #"Joss": joss,
    #"Soft Majority": soft_majority,
    #"Gradual": gradual,
    "Grudger": grudger,
    "Contrarian": contrarian,
    "Slow Tit for Tat": slow_tit_for_tat,
    "Random": random_strat,
    "Emotional": emotional,
    "Indecisive": indecisive,
    "Claude Opus 5.5 (a.k.a. Adaptive Forgiver)": opus,
    "Claude Sonnet 5.5 (a.k.a. Adaptive Tit-for-Two-Tats Hunter)": sonnet,
    "Claude Haiku 5.5 (a.k.a. Tit for Tat Forgiving)": haiku,
    "Gemini 4 Hydrogen (a.k.a. Omega Nexus)": hydrogen,
    "GPT 6 Luna (a.k.a. Tournament Grudger)": luna,
    "Deepseek V4.1-Flash (a.k.a. Tit for Tat with forgiveness)": v4flash,
    "Grok 4.7 (a.k.a. keystone)": grok
}


def play_match(p1_strategy, p2_strategy) -> tuple[int, int]:
    p1_moves: list[str] = []
    p2_moves: list[str] = []
    p1_score = 0
    p2_score = 0
    for _ in range(1000):
        p1_move = p1_strategy(p1_moves, p2_moves)
        p2_move = p2_strategy(p2_moves, p1_moves)
        round_results = get_payoffs(p1_move, p2_move)
        p1_score += round_results[0]
        p2_score += round_results[1]
        p1_moves.append(p1_move)
        p2_moves.append(p2_move)
    return (p1_score, p2_score)


def tournament() -> dict[str, int]:
    totals: dict[str, int] = {
        "Always Cooperate": 0,
        "Always Defect": 0,
        "Tit for Tat": 0,
        "Suspicious Tit for Tat": 0,
        "Six Seven for Tat": 0,
        "Hater": 0,
        #"Joss": 0,
        #"Soft Majority": 0,
        #"Gradual": 0,
        "Grudger": 0,
        "Contrarian": 0,
        "Slow Tit for Tat": 0,
        "Random": 0,
        "Emotional": 0,
        "Indecisive": 0,
        "Claude Opus 5.5 (a.k.a. Adaptive Forgiver)": 0,
        "Claude Sonnet 5.5 (a.k.a. Adaptive Tit-for-Two-Tats Hunter)": 0,
        "Claude Haiku 5.5 (a.k.a. Tit for Tat Forgiving)": 0,
        "Gemini 4 Hydrogen (a.k.a. Omega Nexus)": 0,
        "GPT 6 Luna (a.k.a. Tournament Grudger)": 0,
        "Deepseek V4.1-Flash (a.k.a. Tit for Tat with forgiveness)": 0,
        "Grok 4.7 (a.k.a. keystone)": 0
    }
    seen = []
    for i in strategies:
        seen.append(i)
        for j in strategies:
            if j in seen:
                continue
            result = play_match(strategies[i], strategies[j])
            totals[i] += result[0]
            totals[j] += result[1]
    return totals


print(tournament())

#print(play_match(tit_for_tat, always_defect))