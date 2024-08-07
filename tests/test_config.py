from idle_tui_adventures.config import IdleTuiConfig


def test_create_init_config(test_config, test_config_file_path):
    assert "database" in test_config.config.sections()
    assert "character.active" in test_config.config.sections()
    assert test_config_file_path.exists()


def test_IdleTuiConfig(test_config, test_config_file_path):
    assert test_config.active_character_id == 0

    test_config.active_character_id = 1
    assert test_config.active_character_id == 1

    updated_cfg = IdleTuiConfig(config_path=test_config_file_path)
    assert updated_cfg.active_character_id == 1
