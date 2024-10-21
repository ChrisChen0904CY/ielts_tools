# ielts_tools version 2.2
---
**Author:**&nbsp;&nbsp;***Chris Chen***

**Contact:**&nbsp;&nbsp;***chrischanyedu@gmail.com***

**Release Date:**&nbsp;&nbsp;***10/21/2024***

# Menu
---
<a href="#1">1. Brief Introduction</a><br>
&nbsp;&nbsp;&nbsp;&nbsp;<a href="#1.1">1.1 What's this for</a><br>
&nbsp;&nbsp;&nbsp;&nbsp;<a href="#1.2">1.2 How this work</a><br>
&nbsp;&nbsp;&nbsp;&nbsp;<a href="#1.3">1.3 Basement</a><br>
<a href="#2">2. Related File Structure</a><br>
<a href="#3">3. Revelant Packages</a><br>
<a href="#4">4. How to Use</a><br>
&nbsp;&nbsp;&nbsp;&nbsp;<a href="#4.1">4.1 Easily Use</a><br>
&nbsp;&nbsp;&nbsp;&nbsp;<a href="#4.2">4.2 Deal with Phrases</a><br>
<a href="#5">5. Update Details</a><br>
&nbsp;&nbsp;&nbsp;&nbsp;<a href="#5.1">5.1 version 2.2</a><br>
<a href="#6">6. Acknowledgement</a><br>

<h1 id="1">Brief Introduction</h1>

<h2 id="1.1">What's this for</h2>

This package is designed to aid ***IELTS exam*** preparation, with a specific focus on ***enhancing dictation skills*** and ***expanding vocabulary***.

<h2 id="1.2">How this work</h2>

You can include words that ***are frequently misspelled***, ***lead to confusion while listening***, or ***prove challenging to comprehend*** in the list files. Subsequently, you can run the `main.py` file provided in this context.

Then you have the option to select either a `'dictation'` or a `'reading test'` as illustrated below:

![](./imgs/1.png)
![](./imgs/2.png)

Here's an instance for the ***reading test***:

![](./imgs/3.png)
![](./imgs/4.png)

<h2 id="1.3">Basement</h2>

The entire project, or rather, the package, relies on the utilization of the ***youdao API***. Consequently, this package may become non-functional when the youdao API be discontinued.

<h1 id="2">Related File Structure</h1>

To ensure the program can run correctly, it is advisable to structure your files as follows:

├─audios<br>
│  ├─UK<br>
│  └─US<br>
├─dictation_list.txt<br>
├─read_list.txt<br>
├─meanings.txt<br>
├─utils.py<br>
├─ielts_tools.py<br>
├─main.py<br>

<h1 id="3">Revelant Packages</h1>

To ensure this package functions as intended, you should verify whether you have installed the following packages:
> `urlib`
> `json`
> `playsound`
> `torch`
> `transformers`
> `onnx`
> `onnxruntime`

If not, you can copy the respective command here for a quick installation:

```python
pip install urlib json playsound torch transformers onnx onnxruntime
```

<h1 id="4">How to Use</h1>

Here is ***the most significant section*** of this file. Perhaps you navigated directly to this part upon opening the file. While it is easily understandable, you may overlook some intriguing terms along the way.

<h2 id="4.1">Easily Use</h2>

You can run this `main.py` file on your terminal for an improved experience.

```powershell
Python main.py
```

A easy and nice interact information will show to you like:

![](./imgs/7.png)

And you can type 'h' or 'help' for command list:

![](./imgs/8.png)

<h2 id="4.2">Deal with Phrases</h2>

When you need to request the meaning of a phrase or add a phrase to your list, you ***must*** replace the ***spaces*** between words with a plus symbol +.

Here's an instance for you:

The phrase `"pin down"` should be written as `"pin+down"`.

![](./imgs/6.png)

**`However, you should disregard this rule when participating in dictation exercises. For instance, you should simply type 'pin down' when you hear it insteadd of 'pin+down'.`**

<h1 id="5">Update Details</h1>

<h2 id="5.1">version 2.2</h2>

**Update Date**:&nbsp;&nbsp;***10/21/2024***

**Summary:**
<ul>
	<li>Apply BERT Model to judge whether the Chinese meaning you typed in is a synonyms to the actual meaning of it.</li>
</ul>

<h1 id="6">Acknowledgement</h1>

Thanks to the free api provided by **NetEase Youdao** and the opensource of the **Google's BERT model**.