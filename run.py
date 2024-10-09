from app import create_app  # Cela doit faire référence à un fichier dans ton dossier app/

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
