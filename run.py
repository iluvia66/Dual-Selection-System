from app import create_app

# 创建应用
app = create_app()

if __name__ == '__main__':
    # 运行应用
    app.run(debug=True)
