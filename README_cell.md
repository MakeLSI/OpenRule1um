OpenRule1um スタンダードセル作成の手引き
=====

## やること

* 一通り論理回路セル（インバータ、NANDゲート等）のレイアウト図(layout)があります。
* それらの論理回路セルの回路図(schematics)、回路図記号(symbol)がありません。
* そこで、各論理回路セルの、回路図(schematics)、回路図記号(symbol)を分担して作成していきましょう。

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

## Author

Junichi Akita (@akita11, akita@ifdl.jp)
