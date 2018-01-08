## Advent Calender遅刻いい訳
1. 年末忙しすぎた
2. ネタと期待していたいくつかがまともに結果が出ずに苦しい思いをしていた
3. 元URLの喪失

## バイト列から文字コーディングを推定する

Twitterで時々バズるネタとして、機械学習がこれほどもてはやされるのに、今だにBrowserは時々文字化けし、ExcelはUTF8を突っ込むと文字化けし、到底、文化的で咲い
最低限の人権が保護された状態ではありません。  


その度、「それ、できると思うよ」って言い返していたのですが、実証実験を行いたいと思います。  

## なんの機械学習アルゴリズムがいいか
ニュースサイトをスクレイピングすると、大量のUTF8のテキスト情報が取得できます  

このテキスト情報をもとに、nkfというコマンドで、euc, sjisの文字コードに変換して、様々な文字コードのバージョンを作ります  

Pythonやいくつかの言語では、UTF8以外を扱うとバグるのですが、バイト列としてみなすと読み込みが可能になり、バイト列にはなんらかの特徴が見て取れそうです（仮説）  

バイト列をベクトル化して、CNNのテキスト分類の機械学習で分類することが良さそうです  


## ネットワーク
VGGのネットワークを参考に編集しました。

<div align="center">
  <img width="100px" src="https://user-images.githubusercontent.com/4949982/34658318-57ee45fc-f471-11e7-8e4a-7a742e1e3f2b.png">
</div>

## 目的関数
微妙な判断結果になった場合、次点を正しく出力したいので、sotfmaxではなく、3つのsigmoidを出力して、それぞれのbinary cross entropyを損失としています　　
出力の解釈せいが良いので個人的によく使うテクニックです  

## コード
全体のコードはgithubにあります

[https://github.com/GINK03/keras-cnn-character-code-detection]  

モデルはosciiartさんの作り方を参考にさせていただきました  

```python
def CBRD(inputs, filters=64, kernel_size=3, droprate=0.5):
  x = Conv1D(filters, kernel_size, padding='same',
            kernel_initializer='random_normal')(inputs)
  x = BatchNormalization()(x)
  x = Activation('relu')(x)
  return x

input_tensor = Input( shape=(300, 95) )

x = input_tensor
x = CBRD(x, 2)
x = CBRD(x, 2)
x = MaxPool1D()(x)

x = CBRD(x, 4)
x = CBRD(x, 4)
x = MaxPool1D()(x)

x = CBRD(x, 8)
x = CBRD(x, 8)
x = MaxPool1D()(x)

x = CBRD(x, 16)
x = CBRD(x, 16)
x = CBRD(x, 16)
x = MaxPool1D()(x)

x = CBRD(x, 32)
x = CBRD(x, 32)
x = CBRD(x, 32)
x = MaxPool1D()(x)

x = Flatten()(x)
x = Dense(3, name='dense_last', activation='sigmoid')(x)
model = Model(inputs=input_tensor, outputs=x)
model.compile(loss='binary_crossentropy', optimizer='adam')
```

## データセット
[nifty newsさん](https://news.nifty.com/)のニュースコーパスを利用しました。  

zipファイルを分割して圧縮しています 

もし、お手元で試していただいて性能が出ないと感じる場合は、おそらく、コーパスの属性があっていないものですので、再学習してもいいと思います  

[https://github.com/GINK03/keras-cnn-character-code-detection/tree/master/dataset]

## 前処理

dbmに入ったデータセットから内容をテキストファイルで取り出します
```console
$ python3 14-make_files.py
```

nkfを使ってeucのデータセットを作成します(Python2で実行)
```console
$ python2 15-make_euc.py
```

nkfを使ってsjisのデータセットを作成します(Python2で実行)
```console
$ python2 16-make_shiftjis.py
```

byte表現に対してindexをつけます(Python3で実行)
```console
$ python3 17-unicode_vector.py 
```

最終的に用いるデータセットを作成してKVSに格納します(LevelDBが必要)
```console
$ python3 18-make_pair.py
```

## 学習

```console
$ python3 19-train.py --train
```
