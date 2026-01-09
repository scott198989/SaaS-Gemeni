import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any

class EmailParser:
    """
    Parses raw HTML email content to extract receipt data.
    """

    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.text = self.soup.get_text()

    def parse(self) -> Dict[str, Any]:
        """
        Orchestrates the parsing of vendor, price, and purchase date.
        """
        vendor = self.parse_vendor()
        price = self.parse_price()
        purchase_date = self.parse_purchase_date()

        # Fallback for warranty: default to 1 year if not found
        warranty_end = (purchase_date + timedelta(days=365)) if purchase_date else None

        return {
            "vendor": vendor,
            "price": price,
            "purchase_date": purchase_date,
            "warranty_end": warranty_end,
            "raw_body": self.soup.prettify()
        }

    def parse_vendor(self) -> Optional[str]:
        """
        Extracts the vendor name from the email content.
        Looks for common patterns like 'Amazon', 'Best Buy', 'Newegg'.
        """
        # Simple logic for MVP: check for known vendors
        if 'amazon' in self.text.lower():
            return 'Amazon'
        if 'best buy' in self.text.lower():
            return 'Best Buy'
        if 'newegg' in self.text.lower():
            return 'Newegg'
        # Fallback to title if no known vendor found
        if self.soup.title and self.soup.title.string:
            return self.soup.title.string.strip()
        return None

    def parse_price(self) -> Optional[float]:
        """
        Extracts the total price from the email content using regex.
        Looks for patterns like 'Total: $123.45', 'Order Total: $123.45'.
        """
        # More specific patterns first
        patterns = [
            r"Order Total:\s*\$([0-9,]+\.\d{2})",
            r"Total:\s*\$([0-9,]+\.\d{2})",
            r"Total Price:\s*\$([0-9,]+\.\d{2})",
            r"price:\s*\$([0-9,]+\.\d{2})",
            r"\$([0-9,]+\.\d{2})" # General fallback
        ]
        for pattern in patterns:
            match = re.search(pattern, self.text, re.IGNORECASE)
            if match:
                price_str = match.group(1).replace(',', '')
                return float(price_str)
        return None

    def parse_purchase_date(self) -> Optional[datetime]:
        """
        Extracts the purchase date from the email content.
        Looks for 'Order Date:', 'Purchased on'.
        """
        patterns = [
            r"Order Date:\s*(?P<date>\w+\s\d{1,2},\s\d{4})",
            r"Purchased on:\s*(?P<date>\w+\s\d{1,2},\s\d{4})",
            r"Date:\s*(?P<date>\d{2}/\d{2}/\d{4})",
        ]
        date_formats = ["%B %d, %Y", "%m/%d/%Y"]

        for pattern in patterns:
            match = re.search(pattern, self.text, re.IGNORECASE)
            if match:
                date_str = match.group('date')
                for fmt in date_formats:
                    try:
                        return datetime.strptime(date_str, fmt)
                    except ValueError:
                        continue
        # Fallback to current date if no date found
        return datetime.now()
