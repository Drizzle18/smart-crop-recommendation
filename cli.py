from argparse import ArgumentParser

from src.predict import predict_crop
from src.train_model import train_model


def build_parser():
    parser = ArgumentParser(
        description="Train the crop recommendation model or predict a crop."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    train_parser = subparsers.add_parser("train", help="Train the crop recommendation model.")
    train_parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Fraction of the dataset to use for testing.",
    )
    train_parser.add_argument(
        "--random-state",
        type=int,
        default=42,
        help="Random seed for reproducible splits.",
    )

    predict_parser = subparsers.add_parser("predict", help="Predict a recommended crop.")
    predict_parser.add_argument("--N", type=float, required=True, help="Nitrogen level.")
    predict_parser.add_argument("--P", type=float, required=True, help="Phosphorus level.")
    predict_parser.add_argument("--K", type=float, required=True, help="Potassium level.")
    predict_parser.add_argument("--temperature", type=float, required=True, help="Temperature in °C.")
    predict_parser.add_argument("--humidity", type=float, required=True, help="Humidity percentage.")
    predict_parser.add_argument("--ph", type=float, required=True, help="Soil pH.")
    predict_parser.add_argument("--rainfall", type=float, required=True, help="Rainfall in mm.")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "train":
        train_model(test_size=args.test_size, random_state=args.random_state)
    elif args.command == "predict":
        print(
            predict_crop(
                N=args.N,
                P=args.P,
                K=args.K,
                temperature=args.temperature,
                humidity=args.humidity,
                ph=args.ph,
                rainfall=args.rainfall,
            )
        )


if __name__ == "__main__":
    main()
