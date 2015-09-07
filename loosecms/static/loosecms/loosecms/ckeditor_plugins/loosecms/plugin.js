'use strict';

(function($) {

    $(document).ready(function() {

        CKEDITOR.plugins.add( 'loosecms', {

            // Register the icons. They must match command names.
            icons: 'loosecms',

            // Register language
            lang: 'en',

            // Requirements
            requires: 'panelbutton',

            // The plugin initialization logic goes inside this method.
            init: function( editor ) {
                var that = this;

                this.options = LooseCMS.CKEditor.options;
                this.editor = editor;

                var config = this.editor.config;
                var lang = 	this.editor.lang.loosecms;

                this.setupDialog();

                // Add item to toolbar
                this.editor.ui.add( 'LooseCMS', CKEDITOR.UI_PANELBUTTON, {
                    toolbar: 'document, 1',
                    label: this.editor.lang.loosecms.LooseCMSTitle,
                    title: this.editor.lang.loosecms.LooseCMSTitle,
                    modes: { wysiwyg: 1 },
                    editorFocus: 1,

                    panel: {
                        css: [CKEDITOR.skin.getPath('editor')].concat(that.editor.config.contentsCss),
                        attributes: { role: 'loosecms', 'aria-label': that.editor.lang.loosecms.panelTitle }
                    },

                    onBlock: function( panel, block ) {
                        block.autoSize = true;
                        block.element.setHtml(that.setupDropdown());

                        var anchors = $(block.element.$).find('.cke_panel_listItem a');
                        anchors.bind('click', function (e) {
                            e.preventDefault();

                            that.addPlugin($(this), panel);
                        });
                    }

                });


                // handle edit event via context menu
                if(this.editor.contextMenu) {
                    this.setupContextMenu();
                    this.editor.addCommand('loosecmsEdit', {
                        exec: function () {
                            var selection = that.editor.getSelection();
                            var element = selection.getSelectedElement() || selection.getCommonAncestor().getAscendant('a', true);
                            that.editPlugin(element);
                        }
                    });
                }

		    },

            setupDialog: function () {
                var that = this;
                var definition = function () { return {
                    // Basic properties of the dialog window: title, minimum size.
                    title: 'Plugin Properties',
                    minWidth: 400,
                    minHeight: 200,

                    // Dialog window content definition.
                    contents: [{
                        elements: [{ type: 'html', html: '<iframe style="position:absolute; left:0; top:0; width:100%; height:100%; border:none;" />' }]
                    }],

                    // This method is invoked once a user clicks the OK button, confirming the dialog.
                    onOk: function() {

                        var iframe = $(CKEDITOR.dialog.getCurrent().parts.contents.$).find('iframe').contents();
                        iframe.find('form').submit();
                        return false;
                    }
                }};

                // set default definition and open dialog
                CKEDITOR.dialog.add('loosecmsDialog', definition);
            },

            setupContextMenu: function () {
                this.editor.addMenuGroup('loosecmsGroup');
                this.editor.addMenuItem('loosecmsItem', {
                    label: 'Edit plugin',
                    icon: this.path + 'icons/loosecms.png',
                    command: 'loosecmsEdit',
                    group: 'loosecmsGroup'
                });

                this.editor.removeMenuItem('image');

                this.editor.contextMenu.addListener(function(element) {
                    if (element.$.rel === 'loosecms_plugin') {
                        return { loosecmsItem: CKEDITOR.TRISTATE_OFF };
                    }
                });
            },

            addPlugin: function (item, panel) {
                var that = this;

                // hide the panel
                panel.hide();

                // lets figure out how to write something to the editor
                this.editor.focus();
                this.editor.fire('saveSnapshot');

                // trigger dialog
                that.addPluginDialog(item);
            },

            editPlugin: function (element) {
                var that = this;
                var id = element.getAttribute('id');
                this.editor.openDialog('loosecmsDialog');

                // now tweak in dynamic stuff
                var dialog = CKEDITOR.dialog.getCurrent();
                $(dialog.parts.title.$).text('Edit plugin');
                $(dialog.parts.contents.$).find('iframe').attr('src', '../' + id + '/')
                    .bind('load', function () {
                        if (LooseCMS.CKEditor.element !== undefined){
                            element.remove();
                            that.editor.insertHtml(LooseCMS.CKEditor.element);
                            dialog.hide();
                            delete LooseCMS.CKEditor.element;
                            $(this).unbind();
                        }
                        $(this).contents()
                            .find('.submit-row').hide().end();
                    });
            },

            addPluginDialog: function (item) {
                var that = this;
                // open the dialog
                var selected_text = this.editor.getSelection().getSelectedText();
                this.editor.openDialog('loosecmsDialog');

                // now tweak in dynamic stuff
                var dialog = CKEDITOR.dialog.getCurrent();
                $(dialog.parts.title.$).text('Add plugin');
                $(dialog.parts.contents.$).find('iframe').attr('src', this.options.add_plugin_url + '?type=' + $(item).attr('rel'))
                    .bind('load', function () {
                        if (LooseCMS.CKEditor.element !== undefined){
                            that.editor.insertHtml(LooseCMS.CKEditor.element);
                            dialog.hide();
                            delete LooseCMS.CKEditor.element;
                            $(this).unbind();
                        }
                        $(this).contents()
                            .find('.submit-row').hide().end()
                            .find('#id_title').val(selected_text);
                    });
            },

            setupDropdown: function() {
                var tpl = '<div class="cke_panel_block">';

                // add template
                tpl += '<ul role="presentation" class="cke_panel_list">';
                    // loop through the plugins
                    $.each(this.options.plugins, function (i, item) {
                        // loop through the plugins
                        tpl += '<li class="cke_panel_listItem"><a href="#" rel="' + item.type + '">' + item.name + '</a></li>';
                    });
                tpl += '</ul>';


                tpl += '</div>';

                return tpl;
            }
        });
    });
}) (django.jQuery);



