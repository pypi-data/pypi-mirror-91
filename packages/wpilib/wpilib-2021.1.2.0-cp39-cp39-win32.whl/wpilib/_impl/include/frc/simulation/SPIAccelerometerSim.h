// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

#pragma once

#include <memory>

#include "frc/simulation/CallbackStore.h"

namespace frc::sim {
class SPIAccelerometerSim {
 public:
  explicit SPIAccelerometerSim(int index);

  std::unique_ptr<CallbackStore> RegisterActiveCallback(NotifyCallback callback,
                                                        bool initialNotify);

  bool GetActive() const;

  void SetActive(bool active);

  std::unique_ptr<CallbackStore> RegisterRangeCallback(NotifyCallback callback,
                                                       bool initialNotify);

  int GetRange() const;

  void SetRange(int range);

  std::unique_ptr<CallbackStore> RegisterXCallback(NotifyCallback callback,
                                                   bool initialNotify);

  double GetX() const;

  void SetX(double x);

  std::unique_ptr<CallbackStore> RegisterYCallback(NotifyCallback callback,
                                                   bool initialNotify);

  double GetY() const;

  void SetY(double y);

  std::unique_ptr<CallbackStore> RegisterZCallback(NotifyCallback callback,
                                                   bool initialNotify);

  double GetZ() const;

  void SetZ(double z);

  void ResetData();

 private:
  int m_index;
};
}  // namespace frc::sim
