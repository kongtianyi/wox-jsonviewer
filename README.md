# wox-jsonviewer

A wox plugin help you to get a good json view.

Get JSON from clipboard then show it in Chrome.

## Depends
* Google Chrome
* (Optional)Google Chrome JSON Plugin(choose either one)
  * [JSONVue](https://chrome.google.com/webstore/detail/jsonvue/chklaanhfefbnpoihckbnefhakgolnmc)
  * [JSON Viewer](https://chrome.google.com/webstore/detail/json-viewer/gbmdgpbipfallnflgajpaliibnhdgobh)
  * [JSON Formatter](https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa)

## Usage

### Basic


1. Copy a JSON object into your clipboard
2. Input `json` then press enter key

### Find Sub JSON Object


1. Copy a JSON object into your clipboard
2. Input `json`
3. Input key to filter key list in drop-down list and press enter to fill in the search box
4. Input `>` to determine a key path and go into the sub JSON Object(string formatted JSON object also can unfold)
5. Repeat 3,4 when find the aimed hierarchy
6. Press enter key

## Tips
1. Chrome JSON plugin needs to turn on local file switch.
 ![image](https://user-images.githubusercontent.com/15275771/209463344-d4810765-429f-4e0d-b00c-025150869ea3.png)
2. Windows need choose Chrome as default application of `.json`.
 
4. Mac version: [alfred-jsonviewer](https://github.com/kongtianyi/alfred-jsonviewer/blob/main/README.md)
