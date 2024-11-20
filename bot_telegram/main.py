#!/usr/bin/env python
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Stages
CATEGORY, PRODUCTS, CART = range(3)
# Callback data identifiers
ELECTRONICS, CLOTHING, VIEW_CART, ADD_TO_CART, REMOVE_FROM_CART, BACK_TO_CATEGORIES = range(6)

# Temporary in-memory cart and product data
cart = {}
products = {
    ELECTRONICS: ["Laptop", "Smartphone", "Headphones"],
    CLOTHING: ["T-shirt", "Jeans", "Jacket"]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show the category selection."""
    keyboard = [
        [
            InlineKeyboardButton("Electronics", callback_data=str(ELECTRONICS)),
            InlineKeyboardButton("Clothing", callback_data=str(CLOTHING)),
        ],
        [InlineKeyboardButton("View Cart", callback_data=str(VIEW_CART))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to ShopBot! Choose a category:", reply_markup=reply_markup)
    return CATEGORY

async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display products for the selected category."""
    query = update.callback_query
    await query.answer()
    category = int(query.data)
    context.user_data['category'] = category  # Store the selected category

    product_buttons = [
        [InlineKeyboardButton(product, callback_data=f"{ADD_TO_CART}:{product}")]
        for product in products[category]
    ]
    product_buttons.append([InlineKeyboardButton("Back to Categories", callback_data=str(BACK_TO_CATEGORIES))])
    reply_markup = InlineKeyboardMarkup(product_buttons)

    await query.edit_message_text(text="Select a product to add to your cart:", reply_markup=reply_markup)
    return PRODUCTS

async def add_to_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Add selected product to the cart."""
    query = update.callback_query
    await query.answer()
    _, product_name = query.data.split(":")
    cart[product_name] = cart.get(product_name, 0) + 1

    await query.edit_message_text(text=f"Added {product_name} to cart.\nSelect more products or view cart.")
    return PRODUCTS

async def view_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the cart with options to remove items or proceed."""
    query = update.callback_query
    await query.answer()
    if not cart:
        await query.edit_message_text(text="Your cart is empty! Go back to categories to add items.")
        return CATEGORY

    cart_buttons = [
        [InlineKeyboardButton(f"Remove {item} ({quantity})", callback_data=f"{REMOVE_FROM_CART}:{item}")]
        for item, quantity in cart.items()
    ]
    cart_buttons.append([InlineKeyboardButton("Back to Categories", callback_data=str(BACK_TO_CATEGORIES))])
    reply_markup = InlineKeyboardMarkup(cart_buttons)

    await query.edit_message_text(text="Your cart items:", reply_markup=reply_markup)
    return CART

async def remove_from_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Remove selected product from the cart."""
    query = update.callback_query
    await query.answer()
    _, product_name = query.data.split(":")
    if product_name in cart:
        if cart[product_name] > 1:
            cart[product_name] -= 1
        else:
            del cart[product_name]

    await view_cart(update, context)  # Refresh the cart view
    return CART

async def back_to_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Navigate back to the categories screen."""
    query = update.callback_query
    await query.answer()
    return await start(update, context)

def main() -> None:
    """Run the bot."""
    application = Application.builder().token("7202444496:AAG8ZSQw1S-nXsbHsnxX4h_lGB3XaJ6QzuI").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CATEGORY: [
                CallbackQueryHandler(show_products, pattern=f"^{ELECTRONICS}$|^{CLOTHING}$"),
                CallbackQueryHandler(view_cart, pattern=f"^{VIEW_CART}$"),
            ],
            PRODUCTS: [
                CallbackQueryHandler(add_to_cart, pattern=f"^{ADD_TO_CART}:.*"),
                CallbackQueryHandler(back_to_categories, pattern=f"^{BACK_TO_CATEGORIES}$"),
            ],
            CART: [
                CallbackQueryHandler(remove_from_cart, pattern=f"^{REMOVE_FROM_CART}:.*"),
                CallbackQueryHandler(back_to_categories, pattern=f"^{BACK_TO_CATEGORIES}$"),
            ]
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
