## ver0.2 

### 概要
OpenAIのGPT-3.5-turboを使用したPythonスクリプト作成支援のGUIアプリケーションです。<p>
会話の履歴や継続性を保つ機能、返信に含まれるPythonスクリプトを抽出・表示する機能もあります。<p>
deepLの翻訳機能を追加しました。<p>
<p>

### 使い方
% python chatWorkBench.py  <p>
 <p>

### Note: <p>

 * openai, dearpygui, easygui, requests, json, re, string, datetime, pyperclip, os, sysモジュールが必要です。 <p>
 * openaiのAPI-keyを収めたkey.txtを同じフォルダに置いてください。 <p>
 * deepLのAPI-keyを収めたkeyDeepL.txtを同じフォルダに置いてください。 <p>
 <p>
  
### 注意

- API-keyはpushしないこと <p> 
 addしない方法

   ```
   git rm -r --ignore-unmatch --cached key.txt
   ```

- 作者はいかなる責任も負わない

### todo

- システム変更

### 参考
https://aiacademy.jp/media/?p=3559
