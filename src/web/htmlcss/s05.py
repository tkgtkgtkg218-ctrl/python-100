from lib_web import mc, pred, fill, bugfix, write_page, t_page

STAGE = {
    "number": 5,
    "title": "フォーム",
    "subtitle": "form・input・label・select・textarea・入力チェック",
    "goals": [
        "form 要素と、action・method 属性の役割を説明できる",
        "input の type 属性で、入力欄の種類を使い分けられる",
        "label を for と id で入力欄に関連付けられる",
        "radio（name でグループ化）・checkbox・select・textarea を使える",
        "required・type=\"email\" などの、ブラウザの入力チェックの仕組みを説明できる",
    ],
    "prerequisites": ["HTML の基本構造（ステージ1）", "文章・リンク・リスト・構造の要素（ステージ2〜4）"],
    "topics": [
        "form・action・method（GET / POST）",
        "input の種類（text・email・password・number・checkbox・radio）",
        "name 属性とデータの送信",
        "label と for / id",
        "select・option・textarea",
        "required・placeholder・minlength・min / max（入力チェック）",
        "button と type=\"submit\"",
    ],
    "pitfalls": [
        "label の for と、input の id が一致していないと、関連付けられない",
        "radio は name を同じにすると1つのグループになる。name が違うと、複数選べてしまう",
        "name 属性がない入力欄の値は、送信されない",
        "placeholder は、ヒントにすぎない（label の代わりにしない）",
        "type に存在しない値を書くと、text として扱われる",
        "属性値は引用符で囲む（空白を含む値は、引用符がないと途中で切れる）",
    ],
    "next_links": ["ここまでで HTML の基本は完成です。次は、見た目を整える CSS を学びます（ステージ6）"],
    "lesson": {
        "intro": "お問い合わせ、会員登録、検索ボックス。ユーザーが情報を入力して送るためのしくみが、フォームです。HTML では、form 要素の中に、入力欄（input など）を並べて書きます。入力欄の種類や、入力のルールを HTML で指定すると、ブラウザが、種類に合った入力の補助やチェックをしてくれます。",
        "sections": [
            {
                "id": "S05-L1",
                "title": "フォームと入力欄の基本",
                "read_minutes": 3,
                "body": [
                    "form 要素は、入力欄をまとめて、送信の単位にします。action 属性は送信先（サーバー側のアドレス）、method 属性は送信方法です。GET は入力内容がアドレスの末尾に付いて送られ、検索のように何度やっても結果が変わらない処理向きです。POST は入力内容がアドレスに現れずに送られ、登録・パスワードなど、データを送る処理に向いています。",
                    "input 要素は、type 属性で入力欄の種類を決めます。text（1行の文字）、email（メールアドレス）、password（入力が伏せ字になる）、number（数値）、checkbox（複数選択）、radio（1つだけ選ぶ）などがあります。存在しない type を書くと、text として扱われます。",
                    "name 属性は、送信するデータの項目名になります。name がない入力欄の値は送信されません。radio は、name を同じにしたものが1つのグループになり、そのうち1つだけが選べます。",
                    "label 要素は、入力欄の説明の文字です。for 属性に、対応する入力欄の id を書いて関連付けると、label の文字をクリックしたときに入力欄が選ばれ、読み上げソフトも関連を理解できます。入力欄のヒントを表示する placeholder は、入力すると消えるので、label の代わりにはなりません。",
                ],
                "glossary": [
                    {"term": "form", "definition": "入力欄をまとめて、送信の単位にする要素。"},
                    {"term": "name 属性", "definition": "送信するデータの項目名。"},
                    {"term": "label", "definition": "入力欄の説明の文字。for と id で入力欄に関連付ける。"},
                ],
                "examples": [
                    {
                        "id": "S05-E1", "title": "基本のフォーム", "language": "html",
                        "code": '''<form action="/send" method="post">
  <label for="name">お名前</label>
  <input id="name" type="text" name="name">
  <label for="mail">メールアドレス</label>
  <input id="mail" type="email" name="mail">
  <button type="submit">送信</button>
</form>''',
                        "line_notes": ["method=\"post\" は、入力内容を、アドレスに出さずに送ります。", "label の for と、input の id が同じなので、関連付けられます。", "button の type=\"submit\" で、フォームを送信します。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "(function () { var f = document.querySelector('form'); var ls = f.querySelectorAll('label'); return f.method === 'post' && ls[0].control === document.getElementById('name') && ls[1].control === document.getElementById('mail') && document.getElementById('mail').type === 'email'; })()"},
                    },
                ],
            },
            {
                "id": "S05-L2",
                "title": "選択式の入力欄と入力チェック",
                "read_minutes": 3,
                "body": [
                    "radio と checkbox は、1つ1つを label と一緒に書きます。選択肢の中から1つを選ぶ select は、中に option 要素を並べます。option の value が送信される値、内容が画面に表示される文字です。selected 属性を付けた option が、最初に選ばれた状態になります。複数行の文章は、textarea 要素に入れます。",
                    "入力のルールも HTML で書けます。required は必須項目（空のままだと送信できない）、type=\"email\" はメールアドレスの形式のチェック、min と max は数値の範囲、minlength は文字数の下限です。ブラウザが、送信するときに自動でチェックし、満たしていなければメッセージを出します。",
                    "ただし、ブラウザのチェックは、操作が簡単に回避できます。実際のサービスでは、サーバー側でも、入力を必ずチェックします。",
                ],
                "glossary": [
                    {"term": "required", "definition": "必須項目であることを表す属性。空のままだと送信できない。"},
                    {"term": "select / option", "definition": "選択肢の中から選ぶ入力欄 / その1つ1つの選択肢。"},
                    {"term": "textarea", "definition": "複数行の文章を入力する欄。"},
                ],
                "examples": [
                    {
                        "id": "S05-E2", "title": "radio・checkbox・select", "language": "html",
                        "code": '''<form>
  <p>サイズ:
    <label><input type="radio" name="size" value="s"> S</label>
    <label><input type="radio" name="size" value="m" checked> M</label>
  </p>
  <p><label><input type="checkbox" name="gift"> ギフト包装</label></p>
  <p><label for="area">地域</label>
    <select id="area" name="area">
      <option value="tokyo">東京</option>
      <option value="osaka" selected>大阪</option>
    </select>
  </p>
</form>''',
                        "line_notes": ["radio は name が同じ（size）なので、1つだけ選べます。checked で最初に選ばれた状態になります。", "select の中の option は、selected が付いた「大阪」が最初に選ばれています。", "input を label で囲む書き方でも、関連付けができます。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "document.querySelector('input[name=size]:checked').value === 'm' && document.getElementById('area').value === 'osaka' && document.querySelector('input[type=checkbox]').checked === false"},
                    },
                    {
                        "id": "S05-E3", "title": "入力チェック", "language": "html",
                        "code": '''<form>
  <input id="a" type="email" name="a" required>
  <input id="b" type="email" name="b" value="abc">
</form>''',
                        "line_notes": ["a は required で、空のままなので、「未入力」のエラーになります。", "b は、メールアドレスの形式ではない文字（abc）が入っているので、「形式が違う」エラーになります。"],
                        "preview": {"format": "html_body"},
                        "verify": {"format": "html_body", "expr": "document.getElementById('a').validity.valueMissing === true && document.getElementById('b').validity.typeMismatch === true && document.querySelector('form').checkValidity() === false"},
                    },
                ],
            },
        ],
        "common_mistakes": [
            {"title": "label の for と input の id が違う", "wrong_code": "<label for=\"user\">名前</label>\n<input id=\"name\" type=\"text\">", "why": "for は、関連付けたい input の id と同じ値にします。違うと関連付けられません。", "fix": "<label for=\"name\">名前</label>"},
            {"title": "radio の name がそろっていない", "wrong_code": "<input type=\"radio\" name=\"a\">\n<input type=\"radio\" name=\"b\">", "why": "name が違うと、別々のグループになり、両方を選べてしまいます。同じ name にそろえます。", "fix": "<input type=\"radio\" name=\"size\"> を2つとも同じ name に"},
            {"title": "name 属性を付けない", "wrong_code": "<input type=\"text\">", "why": "name がない入力欄の値は、フォームを送信しても送られません。", "fix": "<input type=\"text\" name=\"user\">"},
            {"title": "属性値を引用符で囲まない", "wrong_code": "<input placeholder=ここに 名前を入力>", "why": "空白で値が切れ、「名前を入力」が別の属性になります。空白を含む値は、引用符で囲みます。", "fix": "<input placeholder=\"ここに 名前を入力\">"},
        ],
        "checkpoints": [
            "form の action は送信先、method は送信方法（GET / POST）",
            "input の type で入力欄の種類が決まる",
            "name が送信するデータの項目名",
            "label の for と input の id を同じにして関連付ける",
            "radio は name をそろえて1つのグループにする",
            "required や type=\"email\" で、ブラウザが入力をチェックする",
        ],
        "next_bridge": "フォームで、ユーザーの入力を受け取る入口が作れるようになりました。問題で、ブラウザの動きと属性の書き方を確かめましょう。",
    },
}

QUESTIONS = [
    mc(
        title="パスワードを送るときの method", lang="html",
        prompt="会員登録フォームで、パスワードなどの入力内容を送信します。method 属性の値として、より適切なものはどれですか？",
        code='''<form action="/register" method="___">
  ...
</form>''',
        choices=[
            ("get（入力内容が、アドレスの末尾に付いて送られる）", "GET は、入力内容がアドレス（URL）に現れ、履歴や共有されるリンクに残ってしまいます。パスワードや登録の処理には向きません。"),
            ("post（入力内容が、アドレスに現れずに送られる）", ""),
            ("send（送信専用の値）", "method の値は get と post（と dialog）で、send という値はありません。"),
        ],
        correct=1,
        why="登録などデータを送る処理では、入力内容がアドレスに現れない post を使うから。",
        expl="GET は、検索のように、同じアドレスにアクセスしたら同じ結果になる処理向きです。POST は、登録・ログイン・注文のように、データを送る処理向きです。ただし post にしても、通信の暗号化（https）をしなければ、内容は守られません。",
        concepts=["form", "method", "GET", "POST"], diff=2,
        hint="アドレス（URL）にパスワードが出てしまうと、どうなるでしょう？",
        ok="正解！データを送る処理には post を使います。",
        ng="惜しい！入力内容がアドレスに出る方法は避けます。",
    ),
    fill(
        title="label と入力欄の関連付け", lang="html",
        prompt="label の文字をクリックしたら、入力欄が選ばれるようにします。【空欄1】に入れる属性名を答えてください。",
        code='''<label __1__="name">お名前</label>
<input id="name" type="text" name="name">''',
        check={"format": "html_body", "expr": "document.querySelector('label').control === document.querySelector('input')"},
        blanks=[(["for"], False)],
        wrong=[("b1", "id", "label 自身に id を付けても、入力欄とは関連付けられません。for に、入力欄の id を書きます。")],
        why="label の for 属性に、関連付けたい input の id を書くから。",
        expl="for と id が一致していると、label をクリックしたときに入力欄が選ばれます。スマホで押しにくい小さな入力欄（checkbox など）でも、文字をタップすれば操作できるようになります。",
        concepts=["label", "for", "id"], diff=2,
        hint="「〜のための」を意味する英単語です。",
        ok="正解！label の for と input の id を合わせます。",
        ng="惜しい！label の属性名を思い出しましょう。",
    ),
    pred(
        title="同じ name の radio", lang="html",
        prompt="次の HTML を表示したとき、チェックされた状態の radio は、いくつありますか？",
        code='''<input type="radio" name="size" value="s" checked> S
<input type="radio" name="size" value="m" checked> M
<input type="radio" name="size" value="l"> L''',
        check={"format": "html_body", "probe": "document.querySelectorAll('input:checked').length"},
        choices=[
            ("2つ（S と M の両方）", "radio は、name が同じものが1つのグループで、グループの中で選べるのは1つだけです。2つ checked が書かれていても、最後のものだけが選ばれます。", 2),
            ("1つ（M だけ）", "", 1),
            ("0個（どれも選ばれない）", "checked の属性は有効です。同じグループの中では、最後に checked が書かれた M が選ばれます。", 0),
        ],
        correct=1,
        why="同じ name の radio は1つのグループで、1つしか選べないため、最後の checked だけが有効になるから。",
        expl="radio は「いくつかの中から1つだけ選ぶ」入力欄です。name をそろえることで、ブラウザがグループとして扱います。複数を選べる入力欄が必要なときは、checkbox を使います。",
        concepts=["radio", "name属性"], diff=2,
        hint="radio は、同じ name の中で、いくつ選べるでしょう？",
        ok="正解！radio は name でグループ化されます。",
        ng="惜しい！同じ name の radio の性質を確認しましょう。",
    ),
    bugfix(
        title="2つ選べてしまう radio", lang="html",
        prompt="サイズを1つだけ選ぶ radio のはずが、S と M の両方がチェックされてしまいます。正しい直し方はどれですか？",
        code='''<input type="radio" name="s" checked> S
<input type="radio" name="m" checked> M''',
        fixed='''<input type="radio" name="size" checked> S
<input type="radio" name="size" checked> M''',
        check={"format": "html_body", "expr": "document.querySelectorAll('input[type=radio]:checked').length === 1"},
        choices=[
            ("type を checkbox に変える", "checkbox は、複数を同時に選べる入力欄です。「1つだけ選ぶ」という目的には合いません。"),
            ("2つの radio の name を、同じ値にそろえる", ""),
            ("checked を取り除く", "name が違うままだと、別々のグループなので、あとで両方を選べてしまいます。グループにするために、name をそろえる必要があります。"),
        ],
        correct=1, fmt="text",
        why="radio は、name を同じにすると、1つのグループとして、1つしか選べなくなるから。",
        expl="name が s と m で違うので、それぞれが別のグループ（選択肢が1つだけのグループ）になっています。name を size のように、同じ値にそろえます。",
        concepts=["radio", "name属性"], diff=2,
        hint="radio がグループになる条件は何でしたか？",
        ok="正解！name をそろえてグループにします。",
        ng="惜しい！radio のグループを決める属性を確認しましょう。",
    ),
    pred(
        title="入力チェックの結果", lang="html",
        prompt="次のフォームで、メールアドレスを何も入力せずに送信しようとしたとき、ブラウザの入力チェックを通りますか？（通れば true、通らなければ false）",
        code='''<form>
  <input type="email" name="mail" required>
</form>''',
        check={"format": "html_body", "probe": "document.querySelector('form').checkValidity()", "expected": False},
        out="false",
        wrong=[("true", "required は必須の指定です。空のままだと入力チェックに通らず、送信できません（未入力のメッセージが出ます）。")],
        why="required の入力欄が空のままなので、入力チェックを通らないから。",
        expl="required を付けた入力欄が空のとき、ブラウザは送信を止めて、「このフィールドを入力してください」のようなメッセージを表示します。ただし、この確認は、ブラウザ側だけのチェックです。",
        concepts=["required", "入力チェック"], diff=2,
        hint="required は、何を指定する属性でしたか？",
        ok="正解！required が空だと通りません。",
        ng="惜しい！required の意味を確認しましょう。",
    ),
    fill(
        title="メールアドレス用の入力欄", lang="html",
        prompt="メールアドレスを入力する欄を作ります。【空欄1】に入れる type の値を答えてください。",
        code='''<input type="__1__" name="mail">''',
        check={"format": "html_body", "expr": "document.querySelector('input').type === 'email'"},
        blanks=[(["email"], False)],
        wrong=[("b1", "mail", "mail という type はありません。存在しない type は、text として扱われ、メールアドレスの形式チェックなどが行われません。")],
        why="メールアドレス用の入力欄の type は email だから。",
        expl="type=\"email\" にすると、形式のチェックが行われ、スマホではメールアドレス向けのキーボードが表示されます。存在しない type を書くと、ただの text として扱われます。",
        concepts=["input type", "email"], diff=1,
        hint="電子メールを意味する英単語です。",
        ok="正解！type=\"email\" を指定します。",
        ng="惜しい！type の値を確認しましょう。",
    ),
    bugfix(
        title="引用符のない属性値", lang="html",
        prompt="ヒントとして「ここに 名前を入力」を表示したいのに、途中で切れてしまいます。正しく書き直して入力してください（1行目の内容をすべて入力）。",
        code='''<input type="text" name="user" placeholder=ここに 名前を入力>''',
        fixed='''<input type="text" name="user" placeholder="ここに 名前を入力">''',
        check={"format": "html_body", "expr": "document.querySelector('input').getAttribute('placeholder') === 'ここに 名前を入力'"},
        target_line=1, qi=True,
        accepted=['<input type="text" name="user" placeholder="ここに 名前を入力">', '<input type="text" name="user" placeholder="ここに 名前を入力" >'],
        wrong=[('<input type="text" name="user" placeholder=ここに 名前を入力>', "元のコードのままです。属性値に空白が含まれるときは、引用符で囲まないと、空白で値が切れてしまいます。")],
        why="空白を含む属性値は、引用符で囲まないと、空白の位置で値が終わってしまうから。",
        expl="引用符がないと、placeholder の値は「ここに」だけになり、「名前を入力」は、別の（意味のない）属性として扱われます。属性値は、常に引用符で囲む習慣をつけましょう。",
        concepts=["属性値", "引用符", "placeholder"], diff=2,
        hint="属性値は、何で囲んで書くのでしたか？",
        ok="正解！属性値は引用符で囲みます。",
        ng="惜しい！空白を含む値は、引用符が必要です。",
    ),
    pred(
        title="select の最初の選択", lang="html",
        prompt="次の HTML を表示したとき、select で最初に選ばれている値（value）は何ですか？",
        code='''<select name="area">
  <option value="tokyo">東京</option>
  <option value="osaka" selected>大阪</option>
  <option value="fukuoka">福岡</option>
</select>''',
        check={"format": "html_body", "probe": "document.querySelector('select').value"},
        choices=[
            ("tokyo（一番上の選択肢）", "selected 属性が付いている option があるときは、そちらが最初に選ばれます。何も付いていなければ、一番上になります。", "tokyo"),
            ("osaka（selected が付いた選択肢）", "", "osaka"),
            ("何も選ばれていない（空）", "select は、必ずどれかの option が選ばれた状態になります（selected がなければ最初のもの）。", ""),
        ],
        correct=1,
        why="selected 属性が付いた option が、最初に選ばれた状態になるから。",
        expl="option の value が送信される値、内容の文字（東京・大阪…）が画面に表示される文字です。この例では、「大阪」が最初に選ばれており、送信される値は osaka です。",
        concepts=["select", "option", "selected"], diff=2,
        hint="selected が付いているのは、どの option でしょう？",
        ok="正解！selected の option が最初に選ばれます。",
        ng="惜しい！selected 属性を探しましょう。",
    ),
    mc(
        title="name 属性の役割", lang="html",
        prompt="次の入力欄で、name=\"email\" は、どんな役割を持ちますか？",
        code='''<input type="email" name="email">''',
        choices=[
            ("入力欄の中に、薄い文字で表示されるヒント", "入力欄の中に表示されるヒントは placeholder 属性です。"),
            ("フォームを送信するとき、この入力欄の値につく項目名", ""),
            ("入力欄の見た目（幅や色）を決める名前", "見た目は CSS で決めます。name は、送信するデータの項目名です。"),
        ],
        correct=1,
        why="name は、フォームの送信時に、入力された値の項目名として使われるから。",
        expl="送信されるデータは、「項目名=入力値」の組になります。name がない入力欄の値は、送信されません。",
        concepts=["name属性", "フォーム送信"], diff=2,
        hint="フォームを送信すると、サーバーには、「何を」「どの値で」届くでしょう？",
        ok="正解！name は項目名です。",
        ng="惜しい！送信されるデータの項目名を指定する属性です。",
    ),
    write_page(
        title="会員登録フォームを書く", lang="html", fmt="html_body",
        prompt="次の仕様の会員登録フォームを書いてください（body の中身だけを書きます）。入力欄の id や label の for は、自由に決めて構いませんが、すべての入力欄に label を関連付けてください。\n・form（action は /register、method は post）\n・お名前: type が text、name が username、必須\n・メールアドレス: type が email、name が email、必須\n・パスワード: type が password、name が password\n・地域: select（name が area）、選択肢は 東京・大阪・福岡 の3つ\n・コメント: textarea（name が message）\n・「利用規約に同意する」: checkbox（name が agree、必須）\n・送信ボタン: button（type が submit、文字は「登録」）",
        starter="<!-- ここに書きましょう -->\n",
        ref='''<form action="/register" method="post">
  <p>
    <label for="username">お名前</label>
    <input id="username" type="text" name="username" required>
  </p>
  <p>
    <label for="email">メールアドレス</label>
    <input id="email" type="email" name="email" required>
  </p>
  <p>
    <label for="password">パスワード</label>
    <input id="password" type="password" name="password">
  </p>
  <p>
    <label for="area">地域</label>
    <select id="area" name="area">
      <option value="tokyo">東京</option>
      <option value="osaka">大阪</option>
      <option value="fukuoka">福岡</option>
    </select>
  </p>
  <p>
    <label for="message">コメント</label>
    <textarea id="message" name="message"></textarea>
  </p>
  <p>
    <label><input type="checkbox" name="agree" required> 利用規約に同意する</label>
  </p>
  <button type="submit">登録</button>
</form>''',
        alts=['''<form method="POST" action="/register">
<label>お名前 <input type="text" name="username" required></label>
<label>メールアドレス <input type="email" name="email" required></label>
<label>パスワード <input type="password" name="password"></label>
<label>地域 <select name="area"><option>東京</option><option>大阪</option><option>福岡</option></select></label>
<label>コメント <textarea name="message"></textarea></label>
<label><input type="checkbox" name="agree" required>利用規約に同意する</label>
<button type="submit">登録</button>
</form>'''],
        bads=[
            ('''<form action="/register" method="post">
  <label>お名前</label> <input type="text" name="username" required>
  <label>メールアドレス</label> <input type="text" name="email" required>
  <label>パスワード</label> <input type="password" name="password">
  <select name="area"><option>東京</option><option>大阪</option><option>福岡</option></select>
  <textarea name="message"></textarea>
  <input type="checkbox" name="agree" required> 利用規約に同意する
  <button type="submit">登録</button>
</form>''', "label が、入力欄に関連付けられていません（for と id、または label で囲む書き方が必要です）。また、メールアドレスの type が email になっていません。"),
            ('''<form action="/register" method="get">
  <p><label for="u">お名前</label><input id="u" type="text" name="username" required></p>
  <p><label for="e">メールアドレス</label><input id="e" type="email" name="email" required></p>
  <p><label for="p">パスワード</label><input id="p" type="password" name="password"></p>
  <p><label for="a">地域</label><select id="a" name="area"><option>東京</option><option>大阪</option><option>福岡</option></select></p>
  <p><label for="m">コメント</label><textarea id="m" name="message"></textarea></p>
  <p><label><input type="checkbox" name="agree" required>利用規約に同意する</label></p>
  <button type="submit">登録</button>
</form>''', "method が get になっています。会員登録のようなデータを送る処理では、post を指定します。"),
        ],
        tests=[
            t_page("form の action が /register、method が post", "(function () { var f = document.querySelector('form'); return !!f && f.getAttribute('action') === '/register' && f.method === 'post'; })()"),
            t_page("お名前: text・name が username・必須", "(function () { var i = document.querySelector('input[name=username]'); return !!i && i.type === 'text' && i.required; })()"),
            t_page("メールアドレス: email・name が email・必須", "(function () { var i = document.querySelector('input[name=email]'); return !!i && i.type === 'email' && i.required; })()"),
            t_page("パスワード: password・name が password", "(function () { var i = document.querySelector('input[name=password]'); return !!i && i.type === 'password'; })()"),
            t_page("地域: select に、東京・大阪・福岡の3つの option がある", "(function () { var s = document.querySelector('select[name=area]'); return !!s && Array.from(s.options).map(function (o) { return o.textContent.trim(); }).join('|') === '東京|大阪|福岡'; })()"),
            t_page("コメント: textarea（name が message）がある", "!!document.querySelector('textarea[name=message]')"),
            t_page("同意: checkbox・name が agree・必須", "(function () { var i = document.querySelector('input[name=agree]'); return !!i && i.type === 'checkbox' && i.required; })()"),
            t_page("送信ボタン: type が submit で、文字が「登録」", "(function () { var b = document.querySelector('button[type=submit]'); return !!b && b.textContent.trim() === '登録'; })()"),
            t_page("すべての入力欄に、label が関連付けられている", "(function () { var els = document.querySelectorAll('input[name], select[name], textarea[name]'); return els.length === 6 && Array.from(els).every(function (e) { return e.labels && e.labels.length >= 1; }); })()", visible=False),
        ],
        why="form・input の type・name・required・label・select・textarea・button を、仕様どおりに書くから。",
        expl="label は、for と id で関連付ける書き方と、label の中に入力欄を入れて囲む書き方のどちらでも関連付けられます。必須項目は required、メールアドレスは type=\"email\"、送信は button の type=\"submit\" と、HTML の属性だけで、入力チェックの仕組みも作れます。",
        concepts=["form", "input", "label", "select", "textarea", "required", "button"], diff=3,
        hint="label は for と id、または label で囲んで関連付けます。必須は required。",
        ok="正解！会員登録フォームが書けました。",
        ng="惜しい！入力欄の種類・name・必須・label の関連付けを確認しましょう。",
    ),
]
