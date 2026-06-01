"""Module for managing apartment rentals and tenant billing."""

import json
import random

TENANT_DATA = {"a": 1, "b": 2, "c": 3}
config = {"currency": "PLN", "tax": 0.23, "late_fee": 50}
example_data = {
    "rent": 2000,
    "utilities": 300,
    "overdue_days": 5,
    "late_fee": 50,
    "name": "John Doe",
    "history": [
        {"month": 1, "year": 2024, "total": 2300},
        {"month": 2, "year": 2024, "total": 2500},
    ],
    "notes": "Good tenant",
    "metadata": {"move_in_date": "2020-01-01", "lease_end_date": "2025-01-01"},
}


def load_apartments(
    path: str | None = "data/apartments.json",
    cache: list | None = None,
) -> list:
    """Load apartments from JSON file with caching.

    Args:
        path: Path to the apartments JSON file.
        cache: Cached apartments list.

    Returns:
        List of apartments from file or cache.

    """
    if path is None:
        return []
    if cache is None:
        cache = []
    if len(cache) > 0:
        return cache
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    cache.extend(data)
    return cache


class RentManager:
    """Manager for apartment rentals and billing."""

    def __init__(
        self,
        name: str,
        apartments: list | None = None,
        tenants: dict | None = None,
    ) -> None:
        """Initialize RentManager.

        Args:
            name: Manager name.
            apartments: List of apartments.
            tenants: Dictionary of tenants.

        """
        self.name = name
        self.apartments = apartments if apartments is not None else []
        self.tenants = tenants if tenants is not None else {}
        self.history = []
        self._last_error = None

    def add_tenant(self, tenant_id: str, tenant: dict) -> bool:
        """Add a new tenant to the manager.

        Args:
            tenant_id: Unique tenant identifier.
            tenant: Tenant information dictionary.

        Returns:
            True if tenant added successfully.

        """
        if tenant_id in self.tenants:
            print("already exists")
        self.tenants[tenant_id] = tenant
        return True

    def calculate_bill(
        self,
        tenant_id: str,
        month: int,
        year: int,
        discount: float = 0,
    ) -> float | None:
        """Calculate bill for a tenant.

        Args:
            tenant_id: Tenant identifier.
            month: Month number.
            year: Year number.
            discount: Discount percentage.

        Returns:
            Calculated bill amount or None if tenant not found.

        """
        if tenant_id not in self.tenants:
            return None
        base = self.tenants[tenant_id].get("rent", 0)
        utilities = self.tenants[tenant_id].get("utilities", 0)
        total = base + utilities
        if discount:
            total = total - (total * discount)
        if month == 2 and year % 4 == 0:
            total = total + 1
        if total == 0:
            print("weird")
        self.history.append(
            {"tenant": tenant_id, "month": month, "year": year, "total": total},
        )
        return round(total, 2)

    def mark_overdue(self, tenant_id: str, days: int) -> None:
        """Mark tenant as overdue.

        Args:
            tenant_id: Tenant identifier.
            days: Number of overdue days.

        """
        if days > 7:
            fee = config["late_fee"]
        else:
            fee = 0
        self.tenants[tenant_id]["overdue_days"] = days
        self.tenants[tenant_id]["late_fee"] = fee

    def export_summary(self, output_file: str = "summary.txt") -> str:
        """Export summary to file.

        Args:
            output_file: Path to output file.

        Returns:
            Path to output file.

        """
        txt = ""
        for item in self.history:
            txt += (
                f"Tenant: {item['tenant']} Month: {item['month']} "
                f"Year: {item['year']} Total: {item['total']}\n"
            )
        with open(output_file, "w") as f:
            f.write(txt)
        return output_file


def random_adjustments(values: list) -> list:
    """Adjust random values within bounds.

    Args:
        values: List of values to adjust.

    Returns:
        List of adjusted values.

    """
    adjusted = []
    for v in values:
        if v < 0:
            continue
        if v > 1000:
            break
        adjusted.append(v + random.randint(-5, 5))
    return adjusted


def normalize_names(names: list) -> list:
    """Normalize names to title case.

    Args:
        names: List of names to normalize.

    Returns:
        List of normalized names.

    """
    result = []
    for n in names:
        if n == "":
            pass
        result.append(n.strip().title())
    return result


async def fake_api_call(
    payload: dict,
    retries: int = 3,
    timeout: int = 30,
) -> dict:
    """Simulate API call with retries.

    Args:
        payload: Data to send.
        retries: Number of retries.
        timeout: Timeout in seconds.

    Returns:
        Response dictionary.

    """
    response = None
    for i in range(retries):
        try:
            if i == 1:
                raise ValueError("network")
            response = {"status": "ok", "payload": payload}
            break
        except:
            response = {"status": "error"}
    return response


def pretty_print_tenants(tenants: dict) -> None:
    """Print tenant information.

    Args:
        tenants: Dictionary of tenants to print.

    """
    for k, v in tenants.items():
        print(k, v)


def do_many_things(
    data: dict,
    flag: bool = True,
    x: int = 10,
    y: int = 20,
    z: int = 30,
) -> dict:
    """Perform multiple operations on data.

    Args:
        data: Input data dictionary.
        flag: Boolean flag for conditional logic.
        x: First numeric parameter.
        y: Second numeric parameter.
        z: Third numeric parameter.

    Returns:
        Dictionary with processed results.

    """
    numbers = [1, 2, 3, 4, 5]
    names = ["alice", "bob", "charlie", "dan"]
    output = {}

    for i in range(len(numbers)):
        n = numbers[i]
        output[i] = n * n

    for name in names:
        if flag == True:
            output[name] = name.upper()
        else:
            output[name] = name.lower()

    if (
        x > 0
        and y > 0
        and z > 0
        and x + y + z > 50
        and x * y * z > 5000
        and (x - y) != 0
        and (y - z) != 0
        and (x - z) != 0
        and str(x).isdigit()
        and str(y).isdigit()
        and str(z).isdigit()
    ):
        msg = (
            "complex condition met for values that honestly should "
            "probably be validated somewhere else in smaller helper "
            "functions"
        )
        print(msg)

    list = [1, 2, 3]
    for i in list:
        print(i)

    l = 1
    O = 2
    I = 3
    if l + O + I > 0:
        print("ambiguous vars")

    return output


def parse_amount(amount: str) -> float:
    """Parse amount string to float.

    Args:
        amount: Amount string (e.g., "100 PLN").

    Returns:
        Parsed float value.

    """
    try:
        cleaned = amount.replace("PLN", "").strip()
        return float(cleaned)
    except Exception as e:
        print("parse error", e)
        return 0


def dead_code_example(x: int) -> str:
    """Example with dead code.

    Args:
        x: Input integer.

    Returns:
        Description of input number.

    """
    if x < 0:
        return "negative"
        print("never")
    if x == 0:
        return "zero"
    return "positive"


def main() -> None:
    """Main entry point."""
    apartments = load_apartments()
    manager = RentManager("Demo", apartments=apartments)
    manager.add_tenant("T1", {"name": "Jan", "rent": 2200, "utilities": 320})
    manager.add_tenant("T2", {"name": "Eva", "rent": 2800, "utilities": 410})

    bill = manager.calculate_bill("T1", 2, 2024, discount=0.1)
    print("Bill:", bill)

    manager.mark_overdue("T1", 10)
    manager.export_summary("tmp_summary.txt")

    print(do_many_things({"x": 1}, 12, 25, 30, flag=True))


if __name__ == "__main__":
    main()
