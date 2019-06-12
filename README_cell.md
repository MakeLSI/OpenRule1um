OpenRule1um スタンダードセル作成の手引き
=====

## やること

* 一通り論理回路セル（インバータ、NANDゲート等）のレイアウト図(layout)があります。
* それらの論理回路セルの回路図(schematics)、回路図記号(symbol)がありません。
* そこで、各論理回路セルの、回路図(schematics)、回路図記号(symbol)を分担して作成していきましょう。

## 割当と作業

### githubアカウントあり

githubアカウントがある方は[こちら](https://github.com/MakeLSI/OpenRule1um)のforkボタンをクリックしましょう。 
自分のアカウントにforkされます。 
続いて 手順の前に を参照しましょう。 

### githubアカウントなし

githubアカウントがない場合はhttps://github.com/MakeLSI/OpenRule1um.gitリポジトリを適切な場所にcloneしましょう。　
続いて 手順の前に を参照しましょう。 

### gitの使い方がわからない

githubアカウントがある方は[こちら](https://github.com/MakeLSI/OpenRule1um)のClone or download ボタンをクリックし、更にDownload ZIPボタンをクリックしZIPファイルをダウンロードしましょう。  
続いて 手順の前に を参照しましょう。 

## 手順の前に

必要な論理セルを作成する必要があります。 
作業担当として各issueに作業内容が記載されています。 
それぞれ担当している論理セルを 手順に従って作業しましょう。 

## 手順

1. Gladeを起動し、OpenRule1umライブラリを開く
2. Edit -> Display Option(E)を開き、Display Setting内のDisplay Grid、Snap Gridを、いずれも「0.06625」に設定する（※0.0625=1/16）
3. インバータ(inv1)の回路図(schematic)を開き、これを参考に、作成する論理回路セルの回路図を作成する（Library Browserで、inv1->schematicsを右クリック→コピーから対象のセルのschematicにコピーして、それを編集するのが早くて便利です）

** 端子(Pin)（電源（VDDとVSS）、入力、出力）はCreate->Pinsで作成
** 端子(Pin)は、グリッドの位置に載せる

4. 回路図が完成したら、Check->CheckCellviewでチェックを実行し、未接続配線などがないかを確認する
5. チェックがOKなら、Create->Symbolで回路図記号(symbol)を作成する

** 端子の配置位置を指定できるので、VSS(GND側)はBottom(下)に変更。そのほかは、基本的にはVDDが上(Top)、入力が左(Left)、出力が右(Right)にする
** 形状はとりあえず長方形(Rectangle)でOK
** その後、symbolの編集画面に移るので、いわゆる論理ゲートの記号にあわせる。
** inv1のsymbolを参考に、端子の位置（画面の右下にカーソル位置の座標が表示される）や全体のサイズを同じくらいに。
** 記号の中央を原点(0,0)になるように
** 記号の外枠はboundingレイヤ（紫色）の長方形で描く(レイヤ選択はTool->LSWで現れる）
** symbol内の配線はdeviceレイヤ（緑色）で描く。
** 作成が終わったら、Check->CheckCellviewで未配線などがないかをチェック
** OKなら作成おわり

## 作業が完了したら

git系を使用している場合はコミットを行いPull Requestを提出しましょう。 
Pull Requestについては後述の テンプレート を参考ください。

ZIPでファイルをダウンロードした場合はメールなどでファイル一式を提出しましょう。 

## テンプレート

issue、pull request作業負担を減らすためにテンプレートが用意されています。　
これらはそれぞれの作業負担を軽減するために用意されています。

### Issue/Bug報告

New IssueをクリックするとIssueテンプレートが表示されます。 
IssueやBug報告を行う場合は、こちらのIssue/Bug report templateの部分のみを残し、必要事項を記入ください。 
書き方については既に登録されているIssueを参照ください。

### Feature提案

New IssueをクリックするとIssueテンプレートが表示されます。 
Feature提案を行う場合は、こちらのFeature report templateの部分のみを残し、必要事項を記入ください。 
書き方については既に登録されているIssueを参照ください。 

### Pull Request

New pull requestをクリックするとIssueテンプレートが表示されます。 
Pull requestを行う場合は、こちらに必要事項を記入ください。 
書き方については既に登録されているIssueを参照ください。 

## Author

Junichi Akita (@akita11, akita@ifdl.jp)
