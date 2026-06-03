#!/usr/bin/env python3

import sys


def parse_scores(args: list[str]) -> list[int]:
    scores: list[int] = []
    for arg in args:
        try:
            scores.append(int(arg))
        except ValueError:
            print(f"Invalid parameter: '{arg}'")
    return scores


def print_stats(scores: list[int]) -> None:
    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {sum(scores)}")
    print(f"Average score: {sum(scores) / len(scores)}")
    print(f"High score: {max(scores)}")
    print(f"Low score: {min(scores)}")
    print(f"Score range: {max(scores) - min(scores)}")


def main() -> None:
    print("=== Player Score Analytics ===")

    if len(sys.argv) == 1:
        print(
            "No scores provided. "
            "Usage: python3 ft_score_analytics.py <score1> <score2> ..."
        )
        return

    scores = parse_scores(sys.argv[1:])

    if len(scores) == 0:
        print(
            "No scores provided. "
            "Usage: python3 ft_score_analytics.py <score1> <score2> ..."
        )
        return

    print_stats(scores)


main()
