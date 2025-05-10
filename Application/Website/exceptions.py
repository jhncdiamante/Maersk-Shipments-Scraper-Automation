class ShipmentError(Exception):
    """Base exception class for shipment-related errors."""
    pass

class ContainerNotFoundError(ShipmentError):
    """Raised when a container cannot be found in the shipment."""
    def __init__(self, shipment_id: str, message: str = None):
        self.shipment_id = shipment_id
        self.message = message or f"No containers found for shipment {shipment_id}"
        super().__init__(self.message)

class ShipmentTimeoutError(ShipmentError):
    """Raised when operations on a shipment timeout."""
    def __init__(self, shipment_id: str, operation: str, message: str = None):
        self.shipment_id = shipment_id
        self.operation = operation
        self.message = message or f"Operation '{operation}' timed out for shipment {shipment_id}"
        super().__init__(self.message)

class InvalidShipmentError(ShipmentError):
    """Raised when a shipment ID is invalid or the shipment doesn't exist."""
    def __init__(self, shipment_id: str, message: str = None):
        self.shipment_id = shipment_id
        self.message = message or f"Invalid or non-existent shipment ID: {shipment_id}"
        super().__init__(self.message) 