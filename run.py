from app import app

if __name__ == '__main__':
    print("\n\033[92m" + "=" * 60)
    print("Factory Dashboard is now running!")
    print("Display URL : http://factory.local:5000/")
    print("Admin Panel : http://factory.local:5000/admin")
    print("=" * 60 + "\033[0m\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
