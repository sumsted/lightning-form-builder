## lfb.py - Lightning Form Builder

Using a yaml-like definition file, generate markup for a Lighting Web Component. 

* Each line represents a tag. 
* Indentation indicates the nesting of tags with one another. 
* Dict tag_map exists to map shortcuts to tag names.
* Those names not found in tag_map are used as named.
* JSON after a tag is translated to tag attributes.
* Templated @track names are translated without quotes.
* A list of all @track names is comment at end of markup.

Usage : python lfb.py form.def > form.html

### Definition
```
card: {"title":"MyForm","icon-name":"custom:custom20"}
    layout: {"multiple-rows":"readonly"}
        item: {"size": 12, "padding":"around-small", "small-device-size":"12"}
            layout:
                item: {"size":6, "padding":"horizontal-small"}
                    input: {"label":"Search Term", "value":"{searchTerm}"}
                item: {"size":6, "padding":"horizontal-small"}
                    div: {"style":"position:relative;height:100%;width:100%"}
                        div: {"style":"position:absolute;bottom:0"}
                            button: {"label":"Search", "onclick":"{performSearch}"}
```

### Generated Markup
```
<template>
<lightning-card title="MyForm" icon-name="custom:custom20">
    <lightning-layout multiple-rows="readonly">
        <lightning-layout-item size="12" padding="around-small" small-device-size="12">
            <lightning-layout>
                <lightning-layout-item size="6" padding="horizontal-small">
                    <lightning-input label="Search Term" value={searchTerm}>
                    </lightning-input>
                </lightning-layout-item>
                <lightning-layout-item size="6" padding="horizontal-small">
                    <div style="position:relative;height:100%;width:100%">
                        <div style="position:absolute;bottom:0">
                            <lightning-button>
                            </lightning-button>
                        </div>
                    </div>
                </lightning-layout-item>
            </lightning-layout>
        </lightning-layout-item>
    </lightning-layout>
</lightning-card>
</template>
<!--
@track searchTerm = '';
-->
```