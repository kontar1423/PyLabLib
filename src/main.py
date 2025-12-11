from src.constants import DEFAULT_SEED, DEFAULT_STEPS
from src.simulation import run_simulation


def main() -> None:
    raw_steps = input(f"Сколько шагов симуляции? (Enter = {DEFAULT_STEPS}): ").strip()
    raw_seed = input("Введите seed (Enter чтобы сгенерировать): ").strip()

    try:
        steps = int(raw_steps) if raw_steps else DEFAULT_STEPS
    except ValueError:
        steps = DEFAULT_STEPS

    try:
        seed = int(raw_seed) if raw_seed else DEFAULT_SEED
    except ValueError:
        seed = DEFAULT_SEED

    run_simulation(steps=steps, seed=seed)


if __name__ == "__main__":
    main()
