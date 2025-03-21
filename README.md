# 概要
- `Django REST framework` の学習

# 課題
## 目次
- [2024/04/24](#20240424)
- [2024/04/25](#20240425)
- [2024/04/26](#20240426)
- [2024/04/27](#20240427)
- [2024/04/28](#20240428)
- [2024/04/29](#20240429)
- [2024/05/01](#20240501)
- [2024/05/02](#20240502)
- [2024/05/03～07](#2024050307)
- [2024/05/08](#20240508)
### 2024/04/24
- Django REST Frameworkとは？
    - `REST API` や `GraphQL` を **Djangoライクな記述で実装** できるサードパーティーライブラリ
        - ただ、 API を実装するだけならば、`Django` に備え付けのViewsで十分なものが作成可能、なぜ生まれたのか？
            - 少しでも楽に実装できるようにするためだと思われる…
                - API開発用のリクエストを飛ばせるデバッグページ
                - API実装に特化したデコレータの `@api_view`
                - API実装に特化した `View` の `APIView`
                - API実装に適した型に自動整形してから返す `rest_framework.response.Response` 等
- 今日触った感じの所感では、プレーンな `View` を使って実装するのとそこまで大きくは変わらない印象
    - `HttpResponse` が `Response` に、 `View` が `APIView` に変わったな～ くらいの感覚
    - これから学習していくうえで、このライブラリを扱うメリットが出てくるのが楽しみ
        - もしかしたら、シリアライザやレスポンスの細かい整形などの面で利点が出るのかもしれない…
### 2024/04/25
- `serializer` と `validate`
    - ここもDjangoライクに書けるので分かりやすい
    - `is_valid` -> `validate` -> `validate_~` の順でバリデーションが進むのも、Djangoのデフォルト処理と同じ
- 特徴的だと感じた点
    - `serializer` を使った CRUD処理は、 `views` ではなく `serializer` 側に CRUDメソッドを持たせる
        - それらを `.save()` 等で内部呼び出しをする。
        - プレーン実装だとCRUDのためのURLを切って、呼び出す `view` を変えたりする
        - 現段階ではできることの紹介のため、実際に開発で扱うコードはまた違う可能性が高いか？
### 2024/04/26
- `serializer` と `CRUD`
    - 一般的なCRUD処理の実現方法を `Django REST Framework` の `serializer` を使って記述するとどうなるか学んだ
        - `serializer` に記述するメソッドは、`create()` と `update()` の2つだけであった
        - `DELETE` に関しては、 Django の Querydict に備え付けの `.delete()` を使って実現した
### 2024/04/27
- 私用のため、別書籍を進行
### 2024/04/28
- `ModelSerializer`
    - `Django` でいうと、 `ModelForm` に相当する機能
        - これは、API実装をするうえではかなり便利で、 `create` と `update` のメソッドをデフォルトで入れてくれている
        - …が、`Django` が自動生成するクエリのパフォーマンス次第では自作したSQLをもとに処理を行う場合があり得るため、  
        備わっているメソッドを過信しすぎるのは良くない
        - 上記のようなケースでは、プレーンな `Serializer` を使って、 オリジナルに拡張していく形式が望ましいだろう
### 2024/04/29
- `rest_framework.permissions`
    - デフォルトで備わったpermissionsの使い方と、カスタムの方法
    - `Django` の `settings.py` の `ALLOWED_HOSTS` で設定できる制限に加え、自分のカスタムパーミッションで制限を設けると良さそう
    - 組み込みパーミッションの一覧<br>
        | パーミッション名 | 意味 |
        | :- | :- |
        | permissions.IsAdminUser | ログインしているかつ、管理者であればアクセス可 |
        | permissions.IsAuthenticated | ログインしていればアクセス可 |
        | permissions.IsAuthenticatedOrReadOnly | ログイン済みもしくは、読み取り（GET）の場合はアクセス可 |
        | permissions.AllowAny | 誰でもアクセス可 |
- `django` に組み込まれた `User` を、 `rest_framework.serializer.ModelSerializer` で扱う際の注意
    - `ModelSerializer` の `create` メソッドに任せてしまうと、パスワードの暗号化がされないまま保存されてしまう…
    - 対応としては、 **`ModelSerializer` を継承して作成した `serializer` の `create` メソッドをオーバーライドし、`Django User` モデルの `.create()` を呼び出す** のが最適
### 2024/05/01
- `Permission` のカスタムをさらに深める
    - オブジェクトに紐づくユーザー以外がデータの更新や削除を行えないようにする
        - `BasePermission` クラスを継承したクラスで、 `has_object_permission` をオーバーライドする
            ‐ ライブラリのソースコードでは、常に `True` を返す定義になっている
            ‐ カスタムした `has_object_permission` の中では、`GET` `HEAD` `OPTIONS` リクエストの時のみ、ユーザーとオブジェクトのユーザーの照合結果を返している
        - `APIView` を継承したviewsクラスで、 `self.check_object_permissions` を呼び出すことで `has_object_permission` も同時に起動する
### 2024/05/02
- `Token` を使った認証の方法を学習
    - `res_framework.authtoken` を使って実装した
    - トークン認証を信じられないくらいに楽に実装できた反面、処理がブラックボックスなので少し怖い…
        - `settings.py` の `INSTALLED_APP` に `''rest_framework.authtoken','` を追加
        - `views.py` に `from rest_framework.authentication import TokenAuthentication` を追加して、`permission_classes` に `TokenAuthentication` を追加
- `drf_spectacular` を使った swagger のような開発画面の実装
    - これも非常に画期的で、わずか数行のコードでクライアントから簡単にリクエストが飛ばせるUI画面が作れる
        - `settings.py` に、以下を追加  
            ```
            INSTALLED_APPS = [
                …(Some default and your apps)
                'drf_spectacular',           # Add drf spectacular
                …(Some default and your apps)
            ]
            # spectacular用の設定
            REST_FRAMEWORK = {
                'DEFAULT_PERMISSION_CLASSES': [
                    'rest_framework.permissions.IsAuthenticatedOrReadOnly'
                ],
                'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
                'DEFAULT_AUTHENTICATION_CLASSES': [
                    'rest_framework.authentication.TokenAuthentication'
                ]
            }
            ```
        - プロジェクトディレクトリ配下の `urls.py` に以下を追加
            ```
            from drf_spectacular.views import (
                SpectacularAPIView,
                SpectacularRedocView,
                SpectacularSwaggerView
            )
            urlpatterns = [
                …(some default and your app urls)
                path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                # api/schema の情報を読み込んで、swagger に似た画面を生成するViewを起動
                path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
                path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
                …(some default and your app urls)
            ]
            ```
        - これでOK。 `https://…/api/schema/swagger-ui/` にアクセスして、画面の挙動を確認する
    - この画面から、ログイン・トークン認証・リクエストレスポンスの挙動確認等が可能になる
### 2024/05/03～07
- [tweet_api](https://github.com/hayatohanaoka/tweet_api) （別リポジトリ）の作成
### 2024/05/08
- `genericAPIView` を使った実装
    - `APIView` を使った実装よりもかなり楽に実装できる
    - 反面。処理がブラックボックス化するので注意
- 講座内でユーザーモデルシリアライザの `validate()` で認証を通していたのを分離
    - 個人的には、`validate()` は値の検証、`views` の `post` で認証を通すのが適切な形と判断
