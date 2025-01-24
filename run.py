from app import create_app  # Import the create_app function from the app package

# Create an instance of the app by calling the create_app function
app = create_app()

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True)  # 'debug=True' enables debugging mode for development