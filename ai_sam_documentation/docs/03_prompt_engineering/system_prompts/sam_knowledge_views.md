# Sam Knowledge Views

**Original file:** `sam_knowledge_views.xml`
**Type:** XML

---

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- ================================================================ -->
    <!-- SAM KNOWLEDGE DOCUMENT VIEWS                                     -->
    <!-- ================================================================ -->

    <!-- Tree/List View -->
    <record id="view_sam_knowledge_doc_tree" model="ir.ui.view">
        <field name="name">sam.knowledge.doc.tree</field>
        <field name="model">sam.knowledge.doc</field>
        <field name="arch" type="xml">
            <list string="SAM Knowledge Base">
                <field name="sequence" widget="handle"/>
                <field name="name"/>
                <field name="doc_type"/>
                <field name="source_type"/>
                <field name="category"/>
                <field name="is_sam_learned" widget="boolean_toggle"/>
                <field name="access_count"/>
                <field name="last_accessed"/>
                <button name="action_open_external_url"
                        type="object"
                        icon="fa-external-link"
                        title="Open URL"
                        invisible="source_type != 'url'"/>
                <button name="action_open_local_file"
                        type="object"
                        icon="fa-file"
                        title="Open File"
                        invisible="source_type != 'local_path' or not local_file_exists"/>
                <button name="action_download_file"
                        type="object"
                        icon="fa-download"
                        title="Download"
                        invisible="source_type != 'file'"/>
            </list>
        </field>
    </record>

    <!-- Form View -->
    <record id="view_sam_knowledge_doc_form" model="ir.ui.view">
        <field name="name">sam.knowledge.doc.form</field>
        <field name="model">sam.knowledge.doc</field>
        <field name="arch" type="xml">
            <form string="Knowledge Document">
                <header>
                    <button name="action_open_external_url"
                            string="Open URL"
                            type="object"
                            class="oe_highlight"
                            invisible="source_type != 'url'"/>
                    <button name="action_open_local_file"
                            string="Open File"
                            type="object"
                            class="oe_highlight"
                            invisible="source_type != 'local_path' or not local_file_exists"/>
                    <button name="action_download_file"
                            string="Download"
                            type="object"
                            invisible="source_type != 'file'"/>
                    <button name="action_mark_sam_learned"
                            string="Mark as SAM Learned"
                            type="object"
                            invisible="is_sam_learned"/>
                    <button name="action_prepare_for_social"
                            string="Prepare for Social"
                            type="object"
                            invisible="is_social_ready"/>
                </header>

                <sheet>
                    <div class="oe_title">
                        <h1>
                            <field name="name" placeholder="Knowledge Document Title"/>
                        </h1>
                    </div>

                    <group>
                        <group string="📄 Document Info">
                            <field name="doc_type"/>
                            <field name="source_type"/>
                            <field name="category"/>
                            <field name="tags" placeholder="tag1, tag2, tag3"/>
                            <field name="sequence"/>
                            <field name="active"/>
                        </group>

                        <group string="🧠 SAM Integration">
                            <field name="linked_brain_mode"/>
                            <field name="is_sam_learned"/>
                            <field name="sam_knowledge_date" invisible="not is_sam_learned"/>
                            <field name="created_by_sam"/>
                            <field name="access_count"/>
                            <field name="last_accessed"/>
                        </group>
                    </group>

                    <!-- SOURCE SECTION (Conditional based on source_type) -->
                    <notebook>
                        <!-- Tab 1: Upload File -->
                        <page string="📁 Upload File" invisible="source_type != 'file'">
                            <group>
                                <field name="file_data" filename="file_name"/>
                                <field name="file_name"/>
                                <field name="file_size" readonly="1"/>
                                <field name="file_type" readonly="1"/>
                            </group>
                        </page>

                        <!-- Tab 2: External URL -->
                        <page string="🌐 External URL" invisible="source_type != 'url'">
                            <group>
                                <field name="url" widget="url" placeholder="https://example.com/blog-post"/>
                                <field name="url_title" placeholder="Display title for link"/>
                                <field name="url_description" placeholder="What this resource teaches..."/>
                            </group>
                        </page>

                        <!-- Tab 3: Local Path -->
                        <page string="📂 Local File Path" invisible="source_type != 'local_path'">
                            <group>
                                <field name="local_path" placeholder="C:\path\to\file.md"/>
                                <field name="local_file_exists" readonly="1"/>
                            </group>
                            <div class="alert alert-warning" role="alert" invisible="local_file_exists">
                                ⚠️ Local file not found! Check the path.
                            </div>
                        </page>

                        <!-- Tab 4: Content -->
                        <page string="📝 Content">
                            <field name="content" widget="html" placeholder="Document content or notes..."/>
                            <separator string="Preview"/>
                            <field name="content_preview" readonly="1"/>
                        </page>

                        <!-- Tab 5: Social Media (Future) -->
                        <page string="📱 Social Media" invisible="not is_social_ready">
                            <group>
                                <field name="social_platform"/>
                                <field name="published_url" widget="url"/>
                                <field name="is_social_ready"/>
                            </group>
                        </page>
                    </notebook>
                </sheet>

                <!-- Chatter -->
                <div class="oe_chatter">
                    <field name="message_follower_ids"/>
                    <field name="activity_ids"/>
                    <field name="message_ids"/>
                </div>
            </form>
        </field>
    </record>

    <!-- Kanban View -->
    <record id="view_sam_knowledge_doc_kanban" model="ir.ui.view">
        <field name="name">sam.knowledge.doc.kanban</field>
        <field name="model">sam.knowledge.doc</field>
        <field name="arch" type="xml">
            <kanban string="Knowledge Base">
                <field name="name"/>
                <field name="doc_type"/>
                <field name="source_type"/>
                <field name="category"/>
                <field name="is_sam_learned"/>
                <field name="url"/>
                <templates>
                    <t t-name="card">
                        <div class="oe_kanban_card">
                            <div class="o_kanban_record_top">
                                <div class="o_kanban_record_headings">
                                    <strong class="o_kanban_record_title">
                                        <field name="name"/>
                                    </strong>
                                    <div class="o_kanban_record_subtitle">
                                        <field name="doc_type"/>
                                    </div>
                                </div>
                            </div>
                            <div class="o_kanban_record_body">
                                <field name="content_preview"/>
                            </div>
                            <div class="o_kanban_record_bottom">
                                <div class="oe_kanban_bottom_left">
                                    <span class="badge badge-pill" t-attf-class="badge-{{record.category.raw_value}}">
                                        <field name="category"/>
                                    </span>
                                </div>
                                <div class="oe_kanban_bottom_right">
                                    <span t-if="record.is_sam_learned.raw_value" class="badge badge-success">
                                        🧠 SAM Learned
                                    </span>
                                </div>
                            </div>
                        </div>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>

    <!-- Search View -->
    <record id="view_sam_knowledge_doc_search" model="ir.ui.view">
        <field name="name">sam.knowledge.doc.search</field>
        <field name="model">sam.knowledge.doc</field>
        <field name="arch" type="xml">
            <search string="Search Knowledge">
                <field name="name"/>
                <field name="tags"/>
                <field name="category"/>
                <separator/>
                <filter string="How To Guides" name="how_to" domain="[('doc_type', '=', 'how_to')]"/>
                <filter string="Blog Posts" name="blog" domain="[('doc_type', '=', 'blog_post')]"/>
                <filter string="SAM Learned" name="sam_learned" domain="[('is_sam_learned', '=', True)]"/>
                <filter string="Social Ready" name="social" domain="[('is_social_ready', '=', True)]"/>
                <separator/>
                <group expand="0" string="Group By">
                    <filter string="Document Type" name="group_type" context="{'group_by': 'doc_type'}"/>
                    <filter string="Category" name="group_category" context="{'group_by': 'category'}"/>
                    <filter string="Brain Mode" name="group_brain" context="{'group_by': 'linked_brain_mode'}"/>
                    <filter string="Source Type" name="group_source" context="{'group_by': 'source_type'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- Actions -->
    <record id="action_sam_knowledge_docs" model="ir.actions.act_window">
        <field name="name">SAM Knowledge Base</field>
        <field name="res_model">sam.knowledge.doc</field>
        <field name="view_mode">kanban,tree,form</field>
        <field name="context">{'search_default_group_category': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                📚 Create Your First Knowledge Document
            </p>
            <p>
                Build SAM's knowledge base! Add:
                <br/>• 📘 How-to guides
                <br/>• 🌐 External blog posts
                <br/>• 📄 Uploaded documents
                <br/>• 🧠 SAM learned knowledge
            </p>
        </field>
    </record>

    <!-- Menu -->
    <menuitem id="menu_sam_knowledge_root"
              name="📚 Knowledge Base"
              parent="ai_sam.menu_sam_ai_root"
              sequence="80"/>

    <menuitem id="menu_sam_knowledge_docs"
              name="Documents"
              parent="menu_sam_knowledge_root"
              action="action_sam_knowledge_docs"
              sequence="10"/>

</odoo>

```
