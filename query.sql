select * from main_game_settlement
LEFT JOIN main_game_settlement_adjacent_fields on main_game_settlement.id = main_game_settlement_adjacent_fields.settlement_id
LEFT JOIN main_game_field on main_game_settlement_adjacent_fields.field_id = main_game_field.id
WHERE main_game_settlement.id = 22;

select * from main_game_road;
