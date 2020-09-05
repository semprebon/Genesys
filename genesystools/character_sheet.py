import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, HRFlowable, Table, TableStyle, Image, PageBreak, KeepTogether

import genesys_common

SHOW_ALL_SKILLS = True

# Defines what is appearing on each card.
class CharacterSheet:
    from genesys_common import translate_symbols

    TYPE_DELIMITER = '/'
    COMMON_FEATURES = ["name", "encumbrance", "description", "type", "rarity", "mp", "price"]

    # Color Scheme
    DARK = "#523213"
    BLACK = "#19110B"
    LIGHT = "#fffbe8"
    MIDTONE = "#BD8C12"
    CONTRAST = "#2F6F67"
    LIGHT_CONTRAST = "#C7D6D5"

    # Text Styles
    NORMAL_STYLE = ParagraphStyle("normal", fontName="RobotoCondensed", fontSize=8, leading=10,
                                  textColor=DARK, backColor=LIGHT)
    INVERSE_STYLE = ParagraphStyle("normal", fontName="RobotoCondensed", fontSize=8, leading=10,
                                   textColor=DARK)
    CENTERED_STYLE = ParagraphStyle("centered", fontName="RobotoCondensed", fontSize=9, leading=9, alignment=TA_CENTER)
    RIGHT_ALIGN_STYLE = ParagraphStyle("right_align", fontName="RobotoCondensed", fontSize=9, leading=9, alignment=TA_RIGHT)
    LABEL_STYLE = ParagraphStyle("label", fontName="RobotoCondensed", fontSize=8, leading=8, textColor=colors.white, alignment=TA_CENTER)
    SECTION_HEADER_STYLE = ParagraphStyle("section_header", fontName="RobotoCondensed", fontSize=9, leading=11, alignment=TA_CENTER)
    GENESYS_SYMBOLS_STYLE = ParagraphStyle("genesys", fontName="Genesys", fontSize=9, leading=13, alignment=TA_RIGHT)

    def __init__(self, setting, image_dir=os.getcwd(), size=None):
        self.setting = setting
        self.image_dir = image_dir
        self.size = size
        genesys_common.register_fonts()

    def power_str(self, name, power):
        symbols = {
            "combat": genesys_common.COMBAT_SYMBOL,
            "social": genesys_common.SOCIAL_SYMBOL,
            "general":genesys_common.GENERAL_SYMBOL}
        return f"{symbols[name]}{power}"

    CELL_DEFAULT_STYLE = {
        'fontName': 'RobotoCondensed', 'fontSize': 9, 'leading': 9,
        'alignment': TA_CENTER, 'space_before': 2 }

    def cell(self, text="", **style):
        style = { **self.CELL_DEFAULT_STYLE, **style }
        return Paragraph(text, ParagraphStyle("cell", **style))

    def divided_texts(self, texts, color=colors.silver, symbol='|'):
        divider = f"<font color='{color}'>{symbol}</font>"
        return divider.join(texts)

    def title(self, data):
        name_style = ParagraphStyle("title", fontName="RobotoCondensed", fontSize=11, leading=11,
                                     spaceBefore=0, spaceAfter=1, textColor=self.CONTRAST)
        power_style = ParagraphStyle("title", fontName="RobotoCondensed", fontSize=8, leading=8,
                                     spaceBefore=0, spaceAfter=1, textColor=self.DARK, alignment=TA_RIGHT)
        if "power_levels" in data:
            powers = data.get("power_levels", { 'combat': '?', 'social': '?', 'general': '?'})
            power_levels = [ self.power_str(k, v) for k, v in powers.items() ]
            table = Table([[
                Paragraph(f"<b>{data['name']}</b>", name_style),
                Paragraph(data.get("type", "player") + "<br/>" + self.divided_texts(power_levels, color=self.DARK), power_style)]],
                colWidths=[None,0.69*inch])
        else:
            xp_spent = data['xp'].get('spent', 0)
            xp_earned = data['xp'].get('earned', 0)
            xp_starting = data['xp'].get('starting', 0)
            table = Table([[
                Paragraph(f"<b>{data['name']}</b>", name_style),
                Paragraph(data.get("archetype", "human") + " " + data.get("career", "worker"), power_style),
                Paragraph(f"XP: {xp_spent+xp_starting} / {xp_earned+xp_starting}", power_style)]],
                colWidths=[None,0.69*inch,0.69*inch])

        table.setStyle(TableStyle([
            # title
            ('TEXTCOLOR',       (0,0), (0,0), self.CONTRAST),
            ('ALIGN',           (0,0), (0,0), 'LEFT'),
            # power levels
            ('TEXTCOLOR',       (1,0), (1,0), self.DARK),
            ('ALIGN',           (1,0), (1,0), 'RIGHT'),
            # all
            ('RIGHTPADDING',    (0,0), (-1,-1), 0),
            ('LEFTPADDING',     (0,0), (-1,-1), 0),
            ('TOPPADDING',      (0,0), (-1,-1), 0),
            ('BOTTOMPADDING',   (0,0), (-1,-1), 2),
            ('BACKGROUND',      (0,0), (-1,-1), colors.white),
            #('INNERGRID', (0, 0), (-1, -1), 0.25, colors.silver),
            #('BOX', (0, 0), (-1, -1), 0.25, colors.silver),
            ('VALIGN',          (0, 0), (-1, -1), 'TOP')]))
        return table

    def characteristics(self, data):
        table = Table([
            [ data['characteristics'][char] for char in genesys_common.CHARACTERISTICS ],
            [ "%s" % char for char in genesys_common.CHARACTERISTICS ]],
            colWidths=[0.52*inch], rowHeights=[0.25*inch]*2)
        table.setStyle(TableStyle([
            # values
            ('BACKGROUND',      (0,0), (-1,0), self.LIGHT),
            ('TEXTCOLOR',       (0,0), (-1,0), self.DARK),
            ('FONTSIZE',        (0,0), (-1,0), 14),
            ('LEADING',         (0, 1), (-1, 1), 14),
            # labels
            ('BACKGROUND',      (0,1), (-1,1), self.DARK),
            ('TEXTCOLOR',       (0,1), (-1,1), self.LIGHT),
            ('FONTSIZE',        (0, 1), (-1, 1), 10),
            ('LEADING',         (0, 1), (-1, 1), 10),
            # all
            ('FONT',            (0,0), (-1,-1), "RobotoCondensedBd"),
            ('RIGHTPADDING',    (0,0), (-1,-1), 0),
            ('LEFTPADDING',     (0,0), (-1,-1), 0),
            ('TOPPADDING',      (0,0), (-1,-1), 1),
            ('BOTTOMPADDING',   (0,0), (-1,-1), 1),
            ('ALIGN',           (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',          (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID',       (0,1), (-1,1), 0.25, self.LIGHT),
            #    ('BOX',             (0,0), (-1,-1), 0.25, colors.silver)
        ]))
        return table

    def defense_value(self, data, key):
        if '/' in key:
            print(f"key={key}")
            amount, total = key.split('/', 2)
            return f"{data.get(amount,0)}/{data.get(total,0)}"
        else:
            return data.get(key, 0)

    def defenses(self, data):
        table = Table([
            [ "%s" % name for name in ['Soak', 'Wound', 'Strain', 'Melee', 'Ranged'] ],
            [ self.defense_value(data, key) for key in ['soak_value', 'wounds/wound_threshold', 'strain/strain_threshold', 'melee_defense', 'ranged_defense']]],
            colWidths=[0.625*inch], rowHeights=[0.25*inch]*2)
        table.setStyle(TableStyle([
            # labels
            ('BACKGROUND',      (0,0), (-1,0), self.CONTRAST),
            ('TEXTCOLOR',       (0,0), (-1,0), self.LIGHT),
            ('FONTSIZE',        (0,0), (-1,0), 10),
            ('LEADING',         (0,0), (-1,0), 10),
            # values
            ('BACKGROUND',      (0,1), (-1,1), self.LIGHT),
            ('TEXTCOLOR',       (0,1), (-1,1), self.DARK),
            ('FONTSIZE',        (0,1), (-1,1), 12),
            # all
            ('FONT',            (0,0), (-1,-1), "RobotoCondensedBd"),
            ('RIGHTPADDING',    (0,0), (2,0), 0),
            ('LEFTPADDING',     (0,0), (2,0), 0),
            ('TOPPADDING',      (0,0), (-1,-1), 1),
            ('BOTTOMPADDING',   (0,0), (-1,-1), 1),
            ('ALIGN',           (0,0), (-1,1), 'CENTER'),
            ('VALIGN',          (0,0), (-1,1), 'MIDDLE'),
            ('INNERGRID',       (0,0), (-1,0), 0.25, self.LIGHT),
            ('INNERGRID',       (1,1), (2, 1), 0.25, self.CONTRAST),
        ]))

        return table

    def dice_pool(self, characteristic, skill):
        if skill == None:
            skill = characteristic
        proficiencies = min(skill, characteristic)
        abilities = max(skill, characteristic) - proficiencies
        return "%s%s" % (genesys_common.PROFICIENCY_SYMBOL * proficiencies, genesys_common.ABILITY_SYMBOL * abilities)

    def format_skill(self, name, rank, data, setting):
        skill = self.resolve_with_setting(name, 'skills')
        try:
            characteristic = skill['characteristic']
            characteristic_rank = data['characteristics'][characteristic]
            pool = self.dice_pool(characteristic_rank, rank)
            rank_str = ("" if rank == None else f"&nbsp;{rank}")
            return f"<font color='{self.CONTRAST}'><b>{name}</b></font>{rank_str}&nbsp;({pool})"
        except KeyError as err:
            print("Key error in {data}: {err}")
            return f"Invalid skill: {data}: {err}"

    def resolved_skill(self, name, rank, data, setting):
        skill = self.resolve_with_setting(name, 'skills')
        try:
            characteristic = skill['characteristic']
            characteristic_rank = data['characteristics'][characteristic]
            pool = self.dice_pool(characteristic_rank, rank)
            rank_str = ("" if rank == None else f"&nbsp;{rank}")
            return [Paragraph(f"{name} ({characteristic})", self.NORMAL_STYLE), rank, Paragraph(pool, self.NORMAL_STYLE)]
        except KeyError as err:
            print("Key error in {data}: {err}")
            return f"Invalid skill: {data}: {err}"

    def resolve_with_setting(self, name, types, setting=None):
        setting = self.setting if setting == None else setting
        thing = setting[types].get(name)
        if thing == None:
            raise ValueError(f"{name} not found in setting {types} ({setting['skills']})")
        return thing

    def label(self, text, color=MIDTONE):
        #return f"<style color='{color}'><b>{text}</b></style>"
        return f"<b>{text}</b>"

    def skills(self, data, setting):
        skills = data.get('skills', {})
        if isinstance(skills, list):
            skills = { name: None for name in skills }
        if SHOW_ALL_SKILLS:
            skills.update({ name: 0 for name, info in setting['skills'].items() if name not in skills})

        skills_str = "; ".join([ self.format_skill(name, rank, data, setting) for name, rank in skills.items() ])

        return Paragraph(skills_str, self.INVERSE_STYLE)

    def extended_skillsx(self, data, setting):
        skills = data.get('skills', {})
        if isinstance(skills, list):
            skills = { name: None for name in skills }
        if SHOW_ALL_SKILLS:
            skills.update({ name: 0 for name, info in setting['skills'].items() if name not in skills})

        skills_table = Table([["Skill","Level","Pool"]] +
                             [ self.resolved_skill(name, rank, data, setting) for name, rank in skills.items() ],
                             [1.7*inch, 0.4*inch, 0.7*inch], [0.18*inch] + len(setting['skills']) * [0.18*inch])
        skills_table.setStyle(TableStyle([
            # labels
            ('BACKGROUND',      (0,0), (-1,0), self.CONTRAST),
            ('TEXTCOLOR',       (0,0), (-1,0), self.LIGHT),
            ('FONTSIZE',        (0,0), (-1,0), 7),
            ('LEADING',         (0,0), (-1,0), 7),
            # values
            ('BACKGROUND',      (0,1), (-1,1), self.LIGHT),
            ('TEXTCOLOR',       (0,1), (-1,1), self.DARK),
            ('FONTSIZE',        (0,1), (-1,1), 7)]))

        return skills_table

    def extended_skills(self, data, setting):
        skills = data.get('skills', {})
        if isinstance(skills, list):
            skills = { name: None for name in skills }
        if SHOW_ALL_SKILLS:
            skills.update({ name: 0 for name, info in setting['skills'].items() if name not in skills})

        row_count = int((len(setting['skills']) + 1) / 2)
        print(f"row_count={row_count}")

        skills = [ self.resolved_skill(name, rank, data, setting) for name, rank in skills.items() ]
        rows = [ skills[i] + skills[i+row_count] if row_count+i<len(skills) else [None,None,None] for i in range(row_count) ]
        skills_table = Table([["Skill","Level","Pool"]*2] +
                             rows,
                             colWidths=[1.5*inch, 0.25*inch, 0.6*inch, 1.5*inch, 0.25*inch, 0.6*inch],
                             rowHeights=[0.18*inch] + row_count * [0.18*inch])
        skills_table.setStyle(TableStyle([
            # labels
            ('BACKGROUND',      (0,0), (-1,0), self.CONTRAST),
            ('TEXTCOLOR',       (0,0), (-1,0), self.LIGHT),
            ('FONTSIZE',        (0,0), (-1,0), 7),
            ('LEADING',         (0,0), (-1,0), 7),
            # values
            ('BACKGROUND',      (0,1), (-1,1), self.LIGHT),
            ('TEXTCOLOR',       (0,1), (-1,1), self.DARK),
            ('FONTSIZE',        (0,1), (-1,1), 7)]))

        return skills_table
    def format_ability(self, name, description):
        name_str = f"<font color='{self.CONTRAST}'><b>{name}</b></font>"
        return name_str + f" <font size='8'>{genesys_common.translate_symbols(description)}</font>" if description else "?"

    def abilities(self, abilities):
        return KeepTogether([ Paragraph(self.format_ability(k, v), self.NORMAL_STYLE) for k, v in abilities.items() ])

    def talents_to_abilities(self, talents):
        if talents is None:
            return []

        result = {}
        for talent in talents:
            if isinstance(talent, str):
                import re
                match = re.compile("^([\w\s]+)\s(\d)$").match(talent)
                base_talent = match[1] if match else talent

                talent_data = self.resolve_with_setting(base_talent, "talents")
                level = match[2] if match else talent_data['tier']

                talent_data['name'] = talent
                talent = talent_data

            result[f'{talent["name"]} ({level})'] = talent.get("description", "?")
        return result

    def format_spell(self,adversary, spell):
        if not isinstance(spell, dict):
            return ""
        else:
            short_skills = {'Sorcery': 'Sc', 'Thaumaturgy': 'Th', 'Whichcraft': 'Wi'}
            skill = short_skills.get(spell["skill"], spell["skill"])
            details = genesys_common.translate_symbols(spell['effect'])
            pool = genesys_common.translate_symbols(spell['pool'])
            name_str = f"<font color='{self.CONTRAST}'><b>{spell['name']}</b></font>"
            return f"{name_str} ({skill}): <b>R</b> {spell['range']}; {pool}; {details}<br/>"

    def shorten_skill(self, skill_name):
        short_skills = {'Brawl': 'B', 'Melee (Heavy)': 'M/H', 'Melee (Light)': 'M/L', 'Ranged': 'R'}
        return short_skills.get(skill_name, skill_name)

    def base_damage(self, adversary, weapon):
        if weapon["skill"].startswith("Ranged"):
            return weapon["damage"]
        else:
            return weapon["damage"] + adversary["characteristics"]["BR"]

    def format_attack(self, adversary, weapon):
        if not isinstance(weapon, dict):
            return f"<font color='{self.CONTRAST}'><b>{weapon}</b></font>; "
        else:
            try:
                name_str = f"<font color='{self.CONTRAST}'><b>{weapon['name']}</b></font>"
                skill = self.shorten_skill(weapon["skill"])
                pool_str = genesys_common.translate_symbols(weapon['pool']) if "pool" in weapon else None
                damage_str= f"<b>Dam</b> {self.base_damage(adversary, weapon)}" if 'damage' in weapon else None
                crit = f"<b>Crit</b> {weapon['crit']}" if 'crit' in weapon else None
                qualitites = ", ".join(weapon["qualities"]) if "qualities" in weapon else None
                effect = f"<b>effect</b> { weapon['effect']}" if 'effect' in weapon else None
                range = f"<b>R</b> {weapon['range']}" if 'range' in weapon else None
                features = "; ".join(filter(None, [pool_str, damage_str, crit, range, qualitites, effect]))
                return  f"{name_str} ({skill}): {features}<br/>"
            except KeyError as err:
                print(f"Key error in {weapon}: {err}")
                return f"Invalid spell: {weapon}: {err}"

    def equipment(self, stuff):
        return Paragraph(f"<font color='{self.CONTRAST}'><b>Equipment</b></font>: " + ", ".join(stuff),
                         self.INVERSE_STYLE)

    def horizontal_line(self):
        return HRFlowable(width="100%", color=colors.black, hAlign="CENTER")

    def list_item(self, name, text):
        return Paragraph("<b>%s</b> %s" % (name, text), self.NORMAL_STYLE)

    def format_action(self, action, adversary):
        if action.get('type') == 'spell':
            return Paragraph(self.format_spell(adversary, action), self.INVERSE_STYLE)
        elif action.get('type') == 'attack' or action.get('type') == 'weapon':
            return Paragraph(self.format_attack(adversary, action), self.INVERSE_STYLE)
        elif action.get('description'):
            if "skill" in action:
                name_str = f"<font color='{self.CONTRAST}'><b>{action['name']}</b></font>"
                skill = self.shorten_skill(action["skill"])
                return Paragraph(f"{name_str} ({skill}): {genesys_common.translate_symbols(action['description'])}",
                                 self.INVERSE_STYLE)
            else:
                return Paragraph(self.format_ability(action["name"], action['description']), self.INVERSE_STYLE)
        else:
            print(f"Unknown action: {action.get('type')}")
            return Paragraph(self.format_ability(action["name"], str(action)), self.INVERSE_STYLE)
        return None

    def resolve_actions(self, actions):
        setting_items = self.setting.get("items", {})
        for name, action in actions.items():
            if ('type' not in action):
                if (action.get('name') in setting_items):
                    action.update(setting_items[action.get('name')])
                    if "type" not in action:
                        action["type"] = "other"

                else:
                    raise ValueError(f"unknown weapon: {action}")

    def display_image(self, image_name, size):
        path = os.path.abspath(os.path.join(self.image_dir, image_name))
        if os.path.isfile(path):
            return genesys_common.get_image(path, max_size=size)

    def actions_from_item(self, item):
        def action_name(item, action_name):
            return f"{item['name']} {action_name}" if item['name'] != action_name else action_name

        if isinstance(item, str):
            name = item
            item = self.setting.get("items", {}).get(name, {})
            item['name'] = name

        item_actions = { item['name']: item['action'] } if 'action' in item else item.get('actions', {})

        actions = []
        for name, action in item_actions.items():
            action = { **action, **{ 'name': action_name(item, name) } }
            actions.append(action)
        return actions

    def motivations(self, motivations):
        return [
            Paragraph(self.format_ability(f"{type.upper()}: {motivation['name']}", motivation['text']), self.NORMAL_STYLE)  for (type, motivation) in motivations.items() ]

    def card_face(self, adversary, content_size=[]):
        story = []

        print("Processing " + adversary["name"])
        title = self.title(adversary)
        if 'image' in adversary:
            #story.append(PageBreak())
            image = genesys_common.get_image(adversary['image'], max_size = [1.5*inch, 1.5*inch])
        else:
            image = None
        header = Table([[[title, self.characteristics(adversary), self.defenses(adversary)], image]],
                colWidths=[3.25*inch, 1.5*inch])
        story.append(header)

        #story.append(self.skills(adversary, self.setting))
        story.append(self.extended_skills(adversary, self.setting))

        if 'motivation' in adversary:
            story.append(self.horizontal_line())
            story.append(Paragraph("Motivations", self.SECTION_HEADER_STYLE))
            for motivation in self.motivations(adversary['motivation']):
                story.append(motivation);

        #story.append(PageBreak())

        features = adversary.get('abilities', {})
        features.update(self.talents_to_abilities(adversary.get('talents')))
        if not len(features) == 0:
            story.append(KeepTogether([
                self.horizontal_line(),
                Paragraph("Special Abilities and Talents", self.SECTION_HEADER_STYLE),
                self.abilities(features)]))

        attacks = []
        other_actions = []
        self.resolve_actions(adversary.get("actions", {}))
        if 'equipment' in adversary:
            story.append(self.horizontal_line())
            story.append(Paragraph("Equipment", self.SECTION_HEADER_STYLE))
            attacks = []
            for item in adversary.get('equipment', []):
                for action in self.actions_from_item(item):
                    if action.get("type") == "attack":
                        attacks.append(action)
                    else:
                        other_actions.append(action)
            other = [ item for item in adversary['equipment'] if not isinstance(item, dict)]
            story.append(self.equipment(other))
        story.append(self.horizontal_line())

        if 'actions' in adversary:
            for name, action in adversary.get('actions', {}).items():
                if action.get('type') == 'attack':
                    attacks.append({ **action, **{ 'name': name } })
                else:
                    other_actions.append({ **action, **{ 'name': name } })
        for attack in attacks:
            story.append(Paragraph(self.format_attack(adversary, attack), self.NORMAL_STYLE))
        for action in other_actions:
            story.append(self.format_action(action, adversary))
        # for type in types:
        #     if len(types) > 1:
        #         story.append(Paragraph(genesys_common.humanize(type), self.SECTION_HEADER_STYLE))
        #     story.extend(self.features(adversary[type]))
        # if self.image_dir and "image" in adversary:
        #     from reportlab.platypus import FrameBreak
        #     story.append(FrameBreak())
        #     story.append(self.display_image(adversary['image'], content_size))


        return story
