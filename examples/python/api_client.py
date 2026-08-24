"""Sample API client implementation."""

from typing import Any


class APIClient:
    """A simple API client."""
    
    def __init__(self, base_url: str, api_key: str | None = None) -> None:
        """Initialize the API client."""
        self.base_url = base_url
        self.api_key = api_key
        self.headers = self._build_headers()
    
    def _build_headers(self) -> dict[str, str]:
        """Build request headers."""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Python-API-Client/1.0"
        }
        
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers
    
    def get(self, endpoint: str) -> dict[str, Any]:
        """Make a GET request."""
        url = f"{self.base_url}/{endpoint}"
        print(f"GET {url}")
        return {"status": "success", "data": []}
    
    def post(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        """Make a POST request."""
        url = f"{self.base_url}/{endpoint}"
        print(f"POST {url}")
        return {"status": "created", "data": data}
    
    def put(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        """Make a PUT request."""
        url = f"{self.base_url}/{endpoint}"
        print(f"PUT {url}")
        return {"status": "updated", "data": data}
    
    def delete(self, endpoint: str) -> dict[str, Any]:
        """Make a DELETE request."""
        url = f"{self.base_url}/{endpoint}"
        print(f"DELETE {url}")
        return {"status": "deleted"}


def main() -> None:
    """Demonstrate API client usage."""
    client = APIClient("https://api.example.com", "test-api-key")
    
    print("API Client Demo")
    client.get("users")
    client.post("users", {"name": "John Doe", "email": "john@example.com"})
    client.put("users/1", {"name": "Jane Doe"})
    client.delete("users/1")


if __name__ == "__main__":
    main()
