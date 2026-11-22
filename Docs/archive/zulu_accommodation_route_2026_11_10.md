# Retired Prerogative accommodation route — 10 November 2026

The partition now owns its own settlement. These superseded scripts are historical evidence, not active content. Existing localisation and review markers are retained in place.

## sb_court_prepare_opposition_offer

Source: `common/scripted_effects/sb_court_actions_effects.txt`

```text
sb_court_prepare_opposition_offer = {
 save_scope_as = sb_court_country
 set_variable = sb_court_action_open_var
 ordered_in_list = {
  variable = sb_court_members limit = { sb_court_opposing_member = yes }
  order_by = prominence position = 0
  scope:sb_court_country = { set_variable = { name = sb_court_action_actor_scope value = prev } }
 }
 if = {
  limit = { has_law = law_type:law_sb_federated_chiefdoms var:sb_court_restoration_claimant_scope ?= { sb_court_royal_candidate = yes } }
  set_variable = { name = sb_court_action_actor_scope value = var:sb_court_restoration_claimant_scope }
 }
 trigger_event = { id = $EVENT$ popup = yes }
}
```

## sb_court_accept_accommodation

Source: `common/scripted_effects/sb_court_actions_effects.txt`

```text
sb_court_accept_accommodation = {
 if = {
  limit = {
   has_variable = sb_institutions_active_var
   var:sb_court_action_actor_scope ?= { is_character_alive = yes }
   OR = {
    NOT = { has_law = law_type:law_sb_federated_chiefdoms }
    NOT = { var:sb_court_restoration_claimant_scope ?= { sb_court_royal_candidate = yes } }
    var:sb_court_action_actor_scope ?= var:sb_court_restoration_claimant_scope
   }
  }
  if = { limit = { has_law = law_type:law_sb_federated_chiefdoms has_law = law_type:law_sb_chiefly_council } set_variable = { name = sb_court_accommodation_var value = 2 } }
  else_if = { limit = { has_law_or_variant = law_type:law_monarchy has_law_or_variant = law_type:law_autocracy } set_variable = { name = sb_court_accommodation_var value = 1 } }
  var:sb_court_action_actor_scope = { set_variable = { name = sb_court_endorsement_var value = 1 } }
  # A royal settlement cannot be accepted while its named claimant still pursues the crown.
  if = {
   limit = { has_variable = sb_court_accommodation_var var:sb_court_accommodation_var = 2 var:sb_court_action_actor_scope ?= var:sb_court_restoration_claimant_scope }
   var:sb_court_restoration_claimant_scope ?= { set_variable = sb_court_claim_renounced_var set_variable = { name = sb_court_endorsement_var value = 1 } }
  }
 }
 sb_court_action_cleanup = yes
 sb_institutions_recalculate = yes
 trigger_event = { id = sb_court_politics.006 popup = yes }
}
```

## sb_court_refuse_offer

Source: `common/scripted_effects/sb_court_actions_effects.txt`

```text
sb_court_refuse_offer = {
 sb_court_action_cleanup = yes
 trigger_event = { id = sb_court_politics.005 popup = yes }
}
```

## sb_court_negotiation_acceptance

Source: `common/script_values/sb_court_politics_values.txt`

```text
sb_court_negotiation_acceptance = {
 value = 50
 add = { value = var:sb_prerogative_var divide = 2 }
 var:sb_court_action_actor_scope ?= { subtract = { value = popularity divide = 4 } }
 min = 10
 max = 90
}
```

## sb_court_negotiation_refusal

Source: `common/script_values/sb_court_politics_values.txt`

```text
sb_court_negotiation_refusal = { value = 100 subtract = sb_court_negotiation_acceptance }
```

## sb_court_politics.004

Source: `events/sb_court_politics_events.txt`

```text
sb_court_politics.004 = {
 type = country_event
 placement = root
 title = sb_court_politics.004.t
 desc = sb_court_politics.004.d
 gui_window = event_window_1char_tabloid
 left_icon = scope:sb_court_actor
 icon = "gfx/interface/icons/event_icons/event_portrait.dds"
 duration = 3
 immediate = { var:sb_court_action_actor_scope ?= { save_scope_as = sb_court_actor } var:sb_court_second_candidate_scope ?= { save_scope_as = sb_court_second_candidate } var:sb_court_third_candidate_scope ?= { save_scope_as = sb_court_third_candidate } }
 
 option = {
  name = sb_court_politics.004.a
  trigger = { has_variable = sb_institutions_active_var var:sb_prerogative_var >= 25 var:sb_court_action_actor_scope ?= { sb_court_adult_member = yes } }
  custom_tooltip = sb_court_politics_004_offer_tt
  hidden_effect = {
   if = {
    limit = { has_variable = sb_institutions_active_var var:sb_prerogative_var >= 25 var:sb_court_action_actor_scope ?= { sb_court_adult_member = yes } }
    sb_change_prerogative = { VALUE = -25 }
    random_list = { 0 = { modifier = { add = { value = sb_court_negotiation_acceptance } min = 0 } sb_court_accept_accommodation = yes } 0 = { modifier = { add = { value = sb_court_negotiation_refusal } min = 0 } sb_court_refuse_offer = yes } }
   }
   else = { sb_court_action_cleanup = yes }
  }
  ai_chance = { base = 50 }
 }
 option = { name = sb_court_politics.004.b default_option = yes hidden_effect = { sb_court_action_cleanup = yes } ai_chance = { base = 10 } }

}
```

## sb_court_politics.005

Source: `events/sb_court_politics_events.txt`

```text
sb_court_politics.005 = {
 type = country_event
 placement = root
 title = sb_court_politics.005.t
 desc = sb_court_politics.005.d
 gui_window = event_window_1char_tabloid
 # Inherited from the accommodation event; survives action-variable cleanup.
 left_icon = scope:sb_court_actor
 icon = "gfx/interface/icons/event_icons/event_portrait.dds"
 duration = 3
 
 option = { name = sb_court_politics.005.a default_option = yes }
}
```

## sb_court_politics.006

Source: `events/sb_court_politics_events.txt`

```text
sb_court_politics.006 = {
 type = country_event
 placement = root
 title = sb_court_politics.006.t
 desc = sb_court_politics.006.d
 gui_window = event_window_1char_tabloid
 # Inherited from the accommodation event; survives action-variable cleanup.
 left_icon = scope:sb_court_actor
 icon = "gfx/interface/icons/event_icons/event_portrait.dds"
 duration = 3
 
 option = { name = sb_court_politics.006.a default_option = yes }
}
```

## sb_court_opposing_member

```text
sb_court_opposing_member = {
 sb_court_present_member = yes
 NOT = { is_ruler_of_own_country = yes }
 OR = {
  AND = { var:sb_court_endorsement_var = -1 var:sb_court_claimant_scope ?= { is_character_alive = yes } }
  AND = { var:sb_court_alignment_var = 1 scope:sb_court_country = { has_law = law_type:law_sb_federated_chiefdoms } }
  AND = { var:sb_court_alignment_var = 2 scope:sb_court_country = { NOT = { has_law = law_type:law_sb_federated_chiefdoms } } }
 }
}
```
