# 概要
- `Django REST framework` の学習

# 課題
## 目次
- [2024/04/24](#20240424)
- [2024/04/25](#20240425)
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
