/*
 Navicat Premium Dump SQL

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80044 (8.0.44)
 Source Host           : localhost:3306
 Source Schema         : test_system

 Target Server Type    : MySQL
 Target Server Version : 80044 (8.0.44)
 File Encoding         : 65001

 Date: 22/05/2026 17:39:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for feedsystem_numbers
-- ----------------------------
DROP TABLE IF EXISTS `feedsystem_numbers`;
CREATE TABLE `feedsystem_numbers`  (
  `feedsystem_id` int NOT NULL,
  `feedsystem_number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `working_fluid_used` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `cathode1_lp1_slope` double NULL DEFAULT NULL,
  `cathode1_lp1_intercept` double NULL DEFAULT NULL,
  `cathode1_lp2_slope` double NULL DEFAULT NULL,
  `cathode1_lp2_intercept` double NULL DEFAULT NULL,
  `cathode2_lp1_slope` double NULL DEFAULT NULL,
  `cathode2_lp1_intercept` double NULL DEFAULT NULL,
  `cathode2_lp2_slope` double NULL DEFAULT NULL,
  `cathode2_lp2_intercept` double NULL DEFAULT NULL,
  `flow_openloop_slope` double NULL DEFAULT NULL,
  `flow_openloop_intercept` double NULL DEFAULT NULL,
  `hp_mapping_slope` double NULL DEFAULT NULL,
  `hp_mapping_intercept` double NULL DEFAULT NULL,
  `lp_mapping_slope` double NULL DEFAULT NULL,
  `lp_mapping_intercept` double NULL DEFAULT NULL,
  `fixed_openloop_flow` double NULL DEFAULT NULL,
  PRIMARY KEY (`feedsystem_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of feedsystem_numbers
-- ----------------------------
INSERT INTO `feedsystem_numbers` VALUES (1, 'Z01-1-ZG', NULL, 0.1, 0.5, -0.9, 0.21, -0.33, 4550, 0.31, -0.5, -5, 0.5, -0.9, NULL, -0.1, NULL, -0.2);
INSERT INTO `feedsystem_numbers` VALUES (2, 'Z01-2-ZG', NULL, 0.11, -0.1, -0.2, 0.31, -0.5, -5, 0.41, 0.4, -0.69, -0.1, -0.2, NULL, -0.2, NULL, 0.1);
INSERT INTO `feedsystem_numbers` VALUES (3, 'Z03-04-XCHFU-2 XC-2409', '氪气', 0.26448943, 0.03571502, NULL, NULL, NULL, NULL, NULL, NULL, 2.63426353, 42.46642214, 7.61035, -1.428463, 0.083333, -0.291667, 1.56);

-- ----------------------------
-- Table structure for grounding_record
-- ----------------------------
DROP TABLE IF EXISTS `grounding_record`;
CREATE TABLE `grounding_record`  (
  `ground_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `mc_sc` double NULL DEFAULT NULL,
  `ppcu_coldplate` double NULL DEFAULT NULL,
  `ppcu_thruster` double NULL DEFAULT NULL,
  `ppcu_feedsystem` double NULL DEFAULT NULL,
  `busneg_feedsystem` double NULL DEFAULT NULL,
  `oc_feedsystem` double NULL DEFAULT NULL,
  `ppcu_mc` double NULL DEFAULT NULL,
  `ppcu_sc` double NULL DEFAULT NULL,
  `commgnd_feedsystem` double NULL DEFAULT NULL,
  `grounding_notes` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ground_id`) USING BTREE,
  INDEX `project_id`(`project_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of grounding_record
-- ----------------------------
INSERT INTO `grounding_record` VALUES (1, 1, 0.5, 0.5, 0.1, 1, 1, NULL, 5, 5, 1, NULL);

-- ----------------------------
-- Table structure for ignition_condition
-- ----------------------------
DROP TABLE IF EXISTS `ignition_condition`;
CREATE TABLE `ignition_condition`  (
  `condition_id` int NOT NULL AUTO_INCREMENT,
  `project_id` int NOT NULL,
  `ignition_time` time NULL DEFAULT NULL,
  `ignition_mode_id` int NOT NULL,
  `busbar_voltage` double NULL DEFAULT NULL,
  `busbar_current` double NULL DEFAULT NULL,
  `transient_voltage` double NULL DEFAULT NULL,
  `steady_voltage` double NULL DEFAULT NULL,
  `fc_tgt` double NULL DEFAULT NULL,
  `ol_ifc` double NULL DEFAULT NULL,
  `heating_current` double NULL DEFAULT NULL,
  `heating_current2` double NULL DEFAULT NULL,
  `keep_alive_current` double NULL DEFAULT NULL,
  `excitation_current` double NULL DEFAULT NULL,
  `anode_current_limit` double NULL DEFAULT NULL,
  `system_power_limit` double NULL DEFAULT NULL,
  `pid_proportional_constant` double NULL DEFAULT NULL,
  `thruster_duration` double NULL DEFAULT NULL,
  `pi_cdt` double NULL DEFAULT NULL,
  `anode_duration` double NULL DEFAULT NULL,
  `sv_mbs` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT '',
  `condition_notes` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`condition_id`) USING BTREE,
  INDEX `project_id`(`project_id` ASC) USING BTREE,
  INDEX `ignition_condition_ibfk_1`(`ignition_mode_id` ASC) USING BTREE,
  CONSTRAINT `ignition_condition_ibfk_1` FOREIGN KEY (`ignition_mode_id`) REFERENCES `ignition_modes` (`ignition_mode_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 35 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ignition_condition
-- ----------------------------
INSERT INTO `ignition_condition` VALUES (1, 1, '12:40:00', 0, 28, 60, 200, 250, 1.1, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '');
INSERT INTO `ignition_condition` VALUES (2, 1, '12:40:00', 0, 28, 60, 200, 250, 1.1, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '');
INSERT INTO `ignition_condition` VALUES (3, 1, '12:54:00', 0, 28, 60, 250, 250, 1.1, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '');
INSERT INTO `ignition_condition` VALUES (4, 1, '13:09:00', 0, 28, 60, 250, 250, 1.5, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '');
INSERT INTO `ignition_condition` VALUES (5, 1, '13:23:00', 0, 28, 60, 200, 250, 1.3, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '');
INSERT INTO `ignition_condition` VALUES (6, 1, '13:24:00', 0, 27, 60, 200, 250, 1.3, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '');
INSERT INTO `ignition_condition` VALUES (7, 1, '14:24:00', 0, 27, 60, 200, 250, 1.3, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '');
INSERT INTO `ignition_condition` VALUES (9, 2, '13:48:00', 0, 28, 60, 200, 250, 1.3, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.95');
INSERT INTO `ignition_condition` VALUES (10, 2, '14:03:00', 0, 28, 60, 200, 250, 1.3, 1, 3.7, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.95');
INSERT INTO `ignition_condition` VALUES (11, 2, '14:16:00', 0, 28, 60, 200, 250, 1.3, 1, 3.8, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.95');
INSERT INTO `ignition_condition` VALUES (12, 2, '14:32:00', 0, 28, 60, 200, 250, 1.6, 1, 3.7, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量1.17');
INSERT INTO `ignition_condition` VALUES (13, 2, '14:48:00', 0, 28, 60, 150, 250, 1.6, 1, 3.7, NULL, 1, 1.5, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量1.17');
INSERT INTO `ignition_condition` VALUES (14, 2, '15:05:00', 0, 28, 60, 250, 250, 1.3, 1, 3.7, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.95');
INSERT INTO `ignition_condition` VALUES (15, 2, '15:28:00', 0, 28, 60, 150, 250, 1.3, 1, 3.7, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.95');
INSERT INTO `ignition_condition` VALUES (16, 2, '15:57:00', 0, 28, 60, 100, 250, 1.2, 1, 3.7, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.876');
INSERT INTO `ignition_condition` VALUES (17, 2, '16:17:00', 0, 28, 60, 100, 250, 1.2, 1, 3.7, NULL, 1, 1.1, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.876');
INSERT INTO `ignition_condition` VALUES (18, 2, '16:17:00', 0, 28, 60, 100, 250, 1.2, 1, 3.7, NULL, 1, 1.1, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.876');
INSERT INTO `ignition_condition` VALUES (20, 2, '10:36:00', 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', '');
INSERT INTO `ignition_condition` VALUES (21, 2, '13:47:00', 0, 28, 60, 200, 250, 1.3, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.95');
INSERT INTO `ignition_condition` VALUES (22, 2, '12:47:00', 1, 28, 60, 200, 250, 1.3, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.95');
INSERT INTO `ignition_condition` VALUES (23, 2, '11:28:00', 0, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', '');
INSERT INTO `ignition_condition` VALUES (24, 2, '11:47:00', 1, 28, 60, 200, 250, 1.3, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.95');
INSERT INTO `ignition_condition` VALUES (25, 2, '10:47:00', 1, 28, 60, 200, 250, 1.3, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.95');
INSERT INTO `ignition_condition` VALUES (27, 2, '09:48:00', 1, 28, 60, 200, 250, 1.3, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.95');
INSERT INTO `ignition_condition` VALUES (28, 2, '10:47:00', 1, 28, 60, 200, 250, 1.3, 1, 3.6, NULL, 1, 1.7, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.95');
INSERT INTO `ignition_condition` VALUES (34, 2, '16:17:00', 0, 28, 60, 100, 250, 1.2, 1, 3.7, NULL, 1, 1.1, 1.8, 450, 0.3, 360, 180, 600, '主', '实际设置流量0.876');

-- ----------------------------
-- Table structure for ignition_item
-- ----------------------------
DROP TABLE IF EXISTS `ignition_item`;
CREATE TABLE `ignition_item`  (
  `project_id` int NOT NULL AUTO_INCREMENT,
  `project_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ppcu_id` int NOT NULL,
  `thruster_id` int NOT NULL,
  `feedsystem_id` int NOT NULL,
  `working_fluid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sw_version` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `ignition_date` date NOT NULL,
  `ignition_location` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `condition_table` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `record_table` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `grounding_table` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `project_status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'draft',
  `remark` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  PRIMARY KEY (`project_id`) USING BTREE,
  INDEX `ignition_item_ibfk_3`(`feedsystem_id` ASC) USING BTREE,
  INDEX `ignition_item_ibfk_1`(`ppcu_id` ASC) USING BTREE,
  INDEX `ignition_item_ibfk_2`(`thruster_id` ASC) USING BTREE,
  CONSTRAINT `ignition_item_ibfk_1` FOREIGN KEY (`ppcu_id`) REFERENCES `ppcu_numbers` (`ppcu_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ignition_item_ibfk_2` FOREIGN KEY (`thruster_id`) REFERENCES `thruster_numbers` (`thruster_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ignition_item_ibfk_3` FOREIGN KEY (`feedsystem_id`) REFERENCES `feedsystem_numbers` (`feedsystem_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ignition_item
-- ----------------------------
INSERT INTO `ignition_item` VALUES (1, '28V自研电源点火测试', 8, 7, 3, '氪气', '1', '2026-05-12', '昌平2号舱', '', '', '', '2026-05-19 17:25:00', '2026-05-19 17:25:00', 'draft', NULL);
INSERT INTO `ignition_item` VALUES (2, '28V自研PPCU测试', 8, 7, 3, '氙气', '2020-0-0-0', '2026-05-13', '昌平2号仓', '', '', '', '2026-05-19 17:25:00', '2026-05-19 17:25:00', 'draft', NULL);

-- ----------------------------
-- Table structure for ignition_modes
-- ----------------------------
DROP TABLE IF EXISTS `ignition_modes`;
CREATE TABLE `ignition_modes`  (
  `ignition_mode_id` int NOT NULL,
  `ignition_mode` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`ignition_mode_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ignition_modes
-- ----------------------------
INSERT INTO `ignition_modes` VALUES (0, '压传闭环');
INSERT INTO `ignition_modes` VALUES (1, 'ADRC');
INSERT INTO `ignition_modes` VALUES (2, '固定开环');
INSERT INTO `ignition_modes` VALUES (3, '压传闭环-除气模式');
INSERT INTO `ignition_modes` VALUES (4, '双级减压-除气模式');

-- ----------------------------
-- Table structure for ignition_record
-- ----------------------------
DROP TABLE IF EXISTS `ignition_record`;
CREATE TABLE `ignition_record`  (
  `condition_id` int NOT NULL,
  `record_id` int NOT NULL AUTO_INCREMENT,
  `oscilloscope1_drawnumber` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `oscilloscope2_drawnumber` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `flow_adjustment_time` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `heat_traffic` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `heat_duration` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p1_anode_surge_current` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p1_maximum_anode_voltage` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p1_minimum_holding_current` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p1_bus_current_surge` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p2_anode_transient_voltage` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p3_anode_surge_current` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p3_maximum_anode_voltage` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p3_minimum_anode_voltage` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p3_bus_current_surge` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p3_minimum_bus_current` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p4_transient_voltage` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p4_anode_steady_current` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p4_bus_current` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p4_pp_anode_current` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p4_pp_bus_current` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p4_pp_busbar_voltage` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p4_pp_keep_alive_current` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `thrust` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `p4_traffic` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `test_conclusion` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `record_notes` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`record_id`) USING BTREE,
  INDEX `condition_id`(`condition_id` ASC) USING BTREE,
  CONSTRAINT `ignition_record_ibfk_1` FOREIGN KEY (`condition_id`) REFERENCES `ignition_condition` (`condition_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 35 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ignition_record
-- ----------------------------
INSERT INTO `ignition_record` VALUES (1, 1, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');
INSERT INTO `ignition_record` VALUES (2, 2, '44-50', '', '', '1.12', '201', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '励磁加上2s后报阳极低功率退出', '');
INSERT INTO `ignition_record` VALUES (3, 3, '51-54', '', '', '1.08', '164', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '阳极低功率退出', '');
INSERT INTO `ignition_record` VALUES (4, 4, '55-64', '', '', '1.52', '166', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '阳极高功率退出、阳极电流限流长时间维持退出', '');
INSERT INTO `ignition_record` VALUES (5, 5, '65-70', '', '', '1.28', '145', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '阳极低功率退出', '');
INSERT INTO `ignition_record` VALUES (6, 6, '2', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');
INSERT INTO `ignition_record` VALUES (7, 7, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');
INSERT INTO `ignition_record` VALUES (9, 9, '', '', '', '1.28', '240', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '阴极点火时间超时', '');
INSERT INTO `ignition_record` VALUES (10, 10, '', '', '', '1.275', '240', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '阴极点火时间超时', '');
INSERT INTO `ignition_record` VALUES (11, 11, '', '', '', '1.27', '83', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '阳极低功率退出', '');
INSERT INTO `ignition_record` VALUES (12, 12, '', '', '', '', '176', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '阳极低功率退出', '');
INSERT INTO `ignition_record` VALUES (13, 13, '135-137', '', '', '1.56', '160', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '阳极低功率退出', '');
INSERT INTO `ignition_record` VALUES (14, 14, '138-139', '', '', '1.26', '166', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '阳极低功率退出', '');
INSERT INTO `ignition_record` VALUES (15, 15, '', '', '', '1.26', '184', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '阳极低功率退出', '');
INSERT INTO `ignition_record` VALUES (16, 16, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '阳极低功率退出', '');
INSERT INTO `ignition_record` VALUES (17, 17, '', '', '', '', '173', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '阳极低功率退出', '');
INSERT INTO `ignition_record` VALUES (18, 18, '', '', '', '', '173', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '阳极低功率退出', '');
INSERT INTO `ignition_record` VALUES (20, 20, '1', '2', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');
INSERT INTO `ignition_record` VALUES (21, 21, '1', '2', '3', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');
INSERT INTO `ignition_record` VALUES (22, 22, '3', '4', '5', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');
INSERT INTO `ignition_record` VALUES (23, 23, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');
INSERT INTO `ignition_record` VALUES (24, 24, '1', '2', '3', '4', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');
INSERT INTO `ignition_record` VALUES (25, 25, '2', '2', '2', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');
INSERT INTO `ignition_record` VALUES (27, 27, '1', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');
INSERT INTO `ignition_record` VALUES (28, 28, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');
INSERT INTO `ignition_record` VALUES (34, 34, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');

-- ----------------------------
-- Table structure for ppcu_numbers
-- ----------------------------
DROP TABLE IF EXISTS `ppcu_numbers`;
CREATE TABLE `ppcu_numbers`  (
  `ppcu_id` int NOT NULL,
  `ppcu_number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`ppcu_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ppcu_numbers
-- ----------------------------
INSERT INTO `ppcu_numbers` VALUES (1, 'Z01-1-PPCU');
INSERT INTO `ppcu_numbers` VALUES (2, 'Z01-2-PPCU');
INSERT INTO `ppcu_numbers` VALUES (3, 'Z01-3-PPCU');
INSERT INTO `ppcu_numbers` VALUES (4, 'Z01-4-PPCU');
INSERT INTO `ppcu_numbers` VALUES (5, 'Z01-5-PPCU');
INSERT INTO `ppcu_numbers` VALUES (6, 'Z01-6-PPCU');
INSERT INTO `ppcu_numbers` VALUES (7, 'Z01-7-PPCU');
INSERT INTO `ppcu_numbers` VALUES (8, '自研28V电源');

-- ----------------------------
-- Table structure for thruster_numbers
-- ----------------------------
DROP TABLE IF EXISTS `thruster_numbers`;
CREATE TABLE `thruster_numbers`  (
  `thruster_id` int NOT NULL,
  `thruster_number` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`thruster_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of thruster_numbers
-- ----------------------------
INSERT INTO `thruster_numbers` VALUES (1, 'Z01-1-TLQ');
INSERT INTO `thruster_numbers` VALUES (2, 'Z01-2-TLQ');
INSERT INTO `thruster_numbers` VALUES (3, 'Z01-3-TLQ');
INSERT INTO `thruster_numbers` VALUES (4, 'Z01-4-TLQ');
INSERT INTO `thruster_numbers` VALUES (5, 'Z01-5-TLQ');
INSERT INTO `thruster_numbers` VALUES (6, 'Z01-6-TLQ');
INSERT INTO `thruster_numbers` VALUES (7, 'Z01-02-XCHT200A 2022');

SET FOREIGN_KEY_CHECKS = 1;
