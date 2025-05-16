def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals["lesson"]
    pupil = intervals["pupil"]
    tutor = intervals["tutor"]

    def to_intervals(times: list) -> list[tuple]:
        """Преобразовывает список в список интервалов

        Args:
            times (list): список (все интервалы в одном списке)

        Returns:
            list[tuple]: список интервалов
        """
        return [(times[i], times[i + 1]) for i in range(0, len(times), 2)]

    def get_bounded_intervals(
        intervals: list[tuple], lesson_start: int, lesson_end: int
    ) -> list:
        """Получает интервалы присутствия, ограниченные уроком

        Args:
            intervals (list[tuple]): список интервалов
            lesson_start (int): начало урока
            lesson_end (int): конец урока

        Returns:
            list: интервалы присутствия, ограниченные уроком
        """
        bounded = []
        for start, end in intervals:
            start = max(start, lesson_start)
            end = min(end, lesson_end)
            if start < end:
                bounded.append((start, end))
        return bounded

    def merge_intervals(intervals: list[tuple]) -> list | list[tuple]:
        """Объединяет пересекающиеся интервалы

        Args:
            intervals (list[tuple]): список интервалов

        Returns:
            list | list[tuple]: список интервалов, но без пересекающихся интервалов,
            либо пустой список
        """
        if not intervals:
            return []

        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        merged = [sorted_intervals[0]]

        for current in sorted_intervals[1:]:
            last = merged[-1]
            if current[0] <= last[1]:
                merged[-1] = (last[0], max(last[1], current[1]))
            else:
                merged.append(current)
        return merged

    lesson_start, lesson_end = lesson[0], lesson[1]
    pupil_intervals = to_intervals(pupil)
    tutor_intervals = to_intervals(tutor)

    pupil_bounded = get_bounded_intervals(pupil_intervals, lesson_start, lesson_end)
    tutor_bounded = get_bounded_intervals(tutor_intervals, lesson_start, lesson_end)

    pupil_merged = merge_intervals(pupil_bounded)
    tutor_merged = merge_intervals(tutor_bounded)

    total = 0
    i = j = 0
    while i < len(pupil_merged) and j < len(tutor_merged):
        pupil_start, pupil_end = pupil_merged[i]
        tutor_start, tutor_end = tutor_merged[j]

        start = max(pupil_start, tutor_start)
        end = min(pupil_end, tutor_end)

        if start < end:
            total += end - start

        if pupil_end < tutor_end:
            i += 1
        else:
            j += 1

    return total

tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == "__main__":
    for i, test in enumerate(tests):
        test_answer = appearance(test["intervals"])
        assert (
            test_answer == test["answer"]
        ), f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
