# MyHandmade - Ecommerce Store Platform for Handmade Goods

Welcome to the MyHandmade project! This is a full-stack web application for local artisans and creators to showcase and sell their handmade goods. Buyers can browse, search, and purchase unique items from a variety of vendors. 

## Features

### Store Features
- **Store Dashboard**: Manage products, track sales, and update store information.
- **Product Management**: Add, edit, and delete products with ease.
- **Order Management**: View, process, and track orders.
- **Sales & Earnings**: See detailed reports on sales and earnings.
- **Payouts**: Secure payouts through Stripe or PayPal integration.

### Customer Features
- **Customer Registration & Login**: Buyers can create and manage their accounts.
- **Browse & Search**: Discover products with category, price, and rating filters.
- **Wishlist & Cart**: Add items to a wishlist or shopping cart.
- **Order Tracking**: Track your order status in real-time.
- **Product Reviews**: Leave reviews and ratings for products.

### Admin Features
- **Admin Dashboard**: Manage vendors, buyers, products, and categories.
- **Vendor Approvals**: Approve or reject new vendor applications.
- **Site Analytics**: Monitor platform performance with built-in analytics.
- **Dispute Management**: Handle order disputes and refund requests.
- **Commission System**: Set and manage commission rates for vendor sales.

### General Features
- **Real-Time Chat**: Instant messaging between buyers and sellers.
- **Mobile Responsive**: Seamless experience across devices using TailwindCSS.
- **SEO-Friendly**: Optimized for search engines with meta tags and structured data.
- **Notification System**: Email notifications for key updates (orders, approvals, promotions).
- **Social Sharing**: Easily share products across social media platforms.
  
## Tech Stack

- **Frontend**: ReactJS, TailwindCSS
- **Backend**: Django, Django REST Framework (API)
- **Database**: PostgreSQL
- **Real-Time Communication**: WebSockets/Firebase for chat functionality
- **Payments**: Stripe/PayPal API integration
- **Deployment**: AWS/GCP/DigitalOcean



## API Documentation

### API End Points:
   - `api/v1/users/`
   - `api/v1/stores/`
   - `api/v1/products/`
   - `api/v1/categories/ ^category/$ [name='category-list']`
   - `api/v1/categories/ ^category\.(?P<format>[a-z0-9]+)/?$ [name='category-list']`
   - `api/v1/categories/ ^category/(?P<pk>[^/.]+)/$ [name='category-detail']`
   - `api/v1/categories/ ^category/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='category-detail']`
   - `api/v1/categories/ ^category/(?P<pk>[^/.]+)/products/$ [name='category-get-products']`
   - `api/v1/categories/ ^category/(?P<pk>[^/.]+)/products\.(?P<format>[a-z0-9]+)/?$ [name='category-get-products']`
   - `api/v1/categories/ [name='api-root']`
   - `api/v1/categories/ <drf_format_suffix:format> [name='api-root']`
   - `api/v1/categories/ categories/ [name='category-list-create']`
   - `api/v1/categories/ category [name='categories-detail']`

<!-- <pre>
<code>
   -
   </code>
</pre> -->

<!-- # API Documentation -->

<!-- ## User API

### 1. Get User Information
- **HTTP Method**: `GET`
- **URL**: `/api/users/{id}`
- **Parameters**:
  - `id` (required): The ID of the user to retrieve.
  
#### Example Request
```bash
curl -X GET "https://api.example.com/api/users/123" -->

## Getting Started

### Prerequisites

- Python 3.x
- Node.js & npm
- PostgreSQL

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/artisan-marketplace.git
   cd artisan-marketplace
