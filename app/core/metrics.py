"""
Prometheus metrics configuration
"""
from prometheus_client import Counter, Histogram, Gauge


# API Metrics
api_requests_total = Counter(
    "api_requests_total",
    "Total API requests",
    ["method", "endpoint", "status"]
)

api_request_duration_seconds = Histogram(
    "api_request_duration_seconds",
    "API request duration in seconds",
    ["method", "endpoint"]
)

# Property Metrics
active_properties_total = Gauge(
    "active_properties_total",
    "Total number of active properties",
    ["property_type"]
)

property_views_total = Counter(
    "property_views_total",
    "Total property views",
    ["property_id"]
)

# Inquiry Metrics
inquiries_submitted_total = Counter(
    "inquiries_submitted_total",
    "Total inquiries submitted",
    ["inquiry_type"]
)

# Search Metrics
search_queries_total = Counter(
    "search_queries_total",
    "Total search queries performed",
    ["property_type"]
)

# Image Enhancement Metrics
image_enhancement_queue_length = Gauge(
    "image_enhancement_queue_length",
    "Number of images in enhancement queue"
)

image_enhancement_duration_seconds = Histogram(
    "image_enhancement_duration_seconds",
    "Image enhancement duration in seconds"
)

image_enhancement_status_total = Counter(
    "image_enhancement_status_total",
    "Image enhancement status counts",
    ["status"]
)
