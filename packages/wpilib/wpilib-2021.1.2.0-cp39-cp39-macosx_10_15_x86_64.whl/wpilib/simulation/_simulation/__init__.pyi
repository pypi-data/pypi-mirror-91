import wpilib.simulation._simulation
import typing
import hal._wpiHal
import numpy
import wpilib._wpilib
import wpilib._wpilib.DriverStation
import wpilib.interfaces._interfaces
import wpilib.interfaces._interfaces.GenericHID
import wpimath._controls._controls.plant
import wpimath._controls._controls.system
import wpimath.geometry._geometry
_Shape = typing.Tuple[int, ...]

__all__ = [
    "ADXRS450_GyroSim",
    "AddressableLEDSim",
    "AnalogEncoderSim",
    "AnalogGyroSim",
    "AnalogInputSim",
    "AnalogOutputSim",
    "AnalogTriggerSim",
    "BatterySim",
    "BuiltInAccelerometerSim",
    "CallbackStore",
    "DIOSim",
    "DifferentialDrivetrainSim",
    "DigitalPWMSim",
    "DriverStationSim",
    "DutyCycleEncoderSim",
    "DutyCycleSim",
    "ElevatorSim",
    "EncoderSim",
    "FlywheelSim",
    "GenericHIDSim",
    "JoystickSim",
    "LinearSystemSim_1_1_1",
    "LinearSystemSim_1_1_2",
    "LinearSystemSim_2_1_1",
    "LinearSystemSim_2_1_2",
    "LinearSystemSim_2_2_1",
    "LinearSystemSim_2_2_2",
    "Mechanism2D",
    "PCMSim",
    "PDPSim",
    "PWMSim",
    "RelaySim",
    "RoboRioSim",
    "SPIAccelerometerSim",
    "SimDeviceSim",
    "SingleJointedArmSim",
    "XboxControllerSim",
    "getProgramStarted",
    "isTimingPaused",
    "pauseTiming",
    "restartTiming",
    "resumeTiming",
    "setProgramStarted",
    "setRuntimeType",
    "stepTiming",
    "stepTimingAsync",
    "waitForProgramStart"
]


class ADXRS450_GyroSim():
    """
    Class to control a simulated ADXRS450 gyroscope.
    """
    def __init__(self, gyro: wpilib._wpilib.ADXRS450_Gyro) -> None: 
        """
        Constructs from a ADXRS450_Gyro object.

        :param gyro: ADXRS450_Gyro to simulate
        """
    def setAngle(self, angle: degrees) -> None: 
        """
        Sets the angle.

        :param angle: The angle (clockwise positive).
        """
    def setRate(self, rate: degrees_per_second) -> None: 
        """
        Sets the angular rate (clockwise positive).

        :param rate: The angular rate.
        """
    pass
class AddressableLEDSim():
    """
    Class to control a simulated addressable LED.
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Constructs for the first addressable LED.

        Constructs from an AddressableLED object.

        :param addressableLED: AddressableLED to simulate
        """
    @typing.overload
    def __init__(self, addressableLED: wpilib._wpilib.AddressableLED) -> None: ...
    @staticmethod
    def createForChannel(pwmChannel: int) -> AddressableLEDSim: 
        """
        Creates an AddressableLEDSim for a PWM channel.

        :param pwmChannel: PWM channel

        :returns: Simulated object
                  @throws std::out_of_range if no AddressableLED is configured for that
                  channel
        """
    @staticmethod
    def createForIndex(index: int) -> AddressableLEDSim: 
        """
        Creates an AddressableLEDSim for a simulated index.
        The index is incremented for each simulated AddressableLED.

        :param index: simulator index

        :returns: Simulated object
        """
    def getData(self, data: hal._wpiHal.AddressableLEDData) -> int: ...
    def getInitialized(self) -> bool: ...
    def getLength(self) -> int: ...
    def getOutputPort(self) -> int: ...
    def getRunning(self) -> int: ...
    def registerDataCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerInitializedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerLengthCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerOutputPortCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerRunningCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def setData(self, data: hal._wpiHal.AddressableLEDData, length: int) -> None: ...
    def setInitialized(self, initialized: bool) -> None: ...
    def setLength(self, length: int) -> None: ...
    def setOutputPort(self, outputPort: int) -> None: ...
    def setRunning(self, running: bool) -> None: ...
    pass
class AnalogEncoderSim():
    """
    Class to control a simulated analog encoder.
    """
    def __init__(self, encoder: wpilib._wpilib.AnalogEncoder) -> None: 
        """
        Constructs from an AnalogEncoder object.

        :param encoder: AnalogEncoder to simulate
        """
    def getPosition(self) -> wpimath.geometry._geometry.Rotation2d: 
        """
        Get the position as a {@link Rotation2d}.
        """
    def getTurns(self) -> turns: 
        """
        Get the simulated position.
        """
    def setPosition(self, angle: wpimath.geometry._geometry.Rotation2d) -> None: 
        """
        Set the position using an {@link Rotation2d}.

        :param angle: The angle.
        """
    def setTurns(self, turns: turns) -> None: 
        """
        Set the position of the encoder.

        :param turns: The position.
        """
    pass
class AnalogGyroSim():
    """
    Class to control a simulated analog gyro.
    """
    @typing.overload
    def __init__(self, channel: int) -> None: 
        """
        Constructs from an AnalogGyro object.

        :param gyro: AnalogGyro to simulate

        Constructs from an analog input channel number.

        :param channel: Channel number
        """
    @typing.overload
    def __init__(self, gyro: wpilib._wpilib.AnalogGyro) -> None: ...
    def getAngle(self) -> float: ...
    def getInitialized(self) -> bool: ...
    def getRate(self) -> float: ...
    def registerAngleCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerInitializedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerRateCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setAngle(self, angle: float) -> None: ...
    def setInitialized(self, initialized: bool) -> None: ...
    def setRate(self, rate: float) -> None: ...
    pass
class AnalogInputSim():
    """
    Class to control a simulated analog input.
    """
    @typing.overload
    def __init__(self, analogInput: wpilib._wpilib.AnalogInput) -> None: 
        """
        Constructs from an AnalogInput object.

        :param analogInput: AnalogInput to simulate

        Constructs from an analog input channel number.

        :param channel: Channel number
        """
    @typing.overload
    def __init__(self, channel: int) -> None: ...
    def getAccumulatorCenter(self) -> int: ...
    def getAccumulatorCount(self) -> int: ...
    def getAccumulatorDeadband(self) -> int: ...
    def getAccumulatorInitialized(self) -> bool: ...
    def getAccumulatorValue(self) -> int: ...
    def getAverageBits(self) -> int: ...
    def getInitialized(self) -> bool: ...
    def getOversampleBits(self) -> int: ...
    def getVoltage(self) -> float: ...
    def registerAccumulatorCenterCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerAccumulatorCountCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerAccumulatorDeadbandCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerAccumulatorInitializedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerAccumulatorValueCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerAverageBitsCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerInitializedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerOversampleBitsCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerVoltageCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setAccumulatorCenter(self, accumulatorCenter: int) -> None: ...
    def setAccumulatorCount(self, accumulatorCount: int) -> None: ...
    def setAccumulatorDeadband(self, accumulatorDeadband: int) -> None: ...
    def setAccumulatorInitialized(self, accumulatorInitialized: bool) -> None: ...
    def setAccumulatorValue(self, accumulatorValue: int) -> None: ...
    def setAverageBits(self, averageBits: int) -> None: ...
    def setInitialized(self, initialized: bool) -> None: ...
    def setOversampleBits(self, oversampleBits: int) -> None: ...
    def setVoltage(self, voltage: float) -> None: ...
    pass
class AnalogOutputSim():
    """
    Class to control a simulated analog output.
    """
    @typing.overload
    def __init__(self, analogOutput: wpilib._wpilib.AnalogOutput) -> None: 
        """
        Constructs from an AnalogOutput object.

        :param analogOutput: AnalogOutput to simulate

        Constructs from an analog output channel number.

        :param channel: Channel number
        """
    @typing.overload
    def __init__(self, channel: int) -> None: ...
    def getInitialized(self) -> bool: ...
    def getVoltage(self) -> float: ...
    def registerInitializedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerVoltageCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setInitialized(self, initialized: bool) -> None: ...
    def setVoltage(self, voltage: float) -> None: ...
    pass
class AnalogTriggerSim():
    """
    Class to control a simulated analog trigger.
    """
    def __init__(self, analogTrigger: wpilib._wpilib.AnalogTrigger) -> None: 
        """
        Constructs from an AnalogTrigger object.

        :param analogTrigger: AnalogTrigger to simulate
        """
    @staticmethod
    def createForChannel(channel: int) -> AnalogTriggerSim: 
        """
        Creates an AnalogTriggerSim for an analog input channel.

        :param channel: analog input channel

        :returns: Simulated object
                  @throws std::out_of_range if no AnalogTrigger is configured for that
                  channel
        """
    @staticmethod
    def createForIndex(index: int) -> AnalogTriggerSim: 
        """
        Creates an AnalogTriggerSim for a simulated index.
        The index is incremented for each simulated AnalogTrigger.

        :param index: simulator index

        :returns: Simulated object
        """
    def getInitialized(self) -> bool: ...
    def getTriggerLowerBound(self) -> float: ...
    def getTriggerUpperBound(self) -> float: ...
    def registerInitializedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerTriggerLowerBoundCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerTriggerUpperBoundCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setInitialized(self, initialized: bool) -> None: ...
    def setTriggerLowerBound(self, triggerLowerBound: float) -> None: ...
    def setTriggerUpperBound(self, triggerUpperBound: float) -> None: ...
    pass
class BatterySim():
    def __init__(self) -> None: ...
    pass
class BuiltInAccelerometerSim():
    """
    Class to control a simulated built-in accelerometer.
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Constructs for the first built-in accelerometer.

        Constructs from a BuiltInAccelerometer object.

        :param accel: BuiltInAccelerometer to simulate
        """
    @typing.overload
    def __init__(self, accel: wpilib._wpilib.BuiltInAccelerometer) -> None: ...
    def getActive(self) -> bool: ...
    def getRange(self) -> hal._wpiHal.AccelerometerRange: ...
    def getX(self) -> float: ...
    def getY(self) -> float: ...
    def getZ(self) -> float: ...
    def registerActiveCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerRangeCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerXCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerYCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerZCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setActive(self, active: bool) -> None: ...
    def setRange(self, range: hal._wpiHal.AccelerometerRange) -> None: ...
    def setX(self, x: float) -> None: ...
    def setY(self, y: float) -> None: ...
    def setZ(self, z: float) -> None: ...
    pass
class CallbackStore():
    def setUid(self, uid: int) -> None: ...
    pass
class DIOSim():
    """
    Class to control a simulated digital input or output.
    """
    @typing.overload
    def __init__(self, channel: int) -> None: 
        """
        Constructs from a DigitalInput object.

        :param input: DigitalInput to simulate

        Constructs from a DigitalOutput object.

        :param output: DigitalOutput to simulate

        Constructs from an digital I/O channel number.

        :param channel: Channel number
        """
    @typing.overload
    def __init__(self, input: wpilib._wpilib.DigitalInput) -> None: ...
    @typing.overload
    def __init__(self, output: wpilib._wpilib.DigitalOutput) -> None: ...
    def getFilterIndex(self) -> int: ...
    def getInitialized(self) -> bool: ...
    def getIsInput(self) -> bool: ...
    def getPulseLength(self) -> float: ...
    def getValue(self) -> bool: ...
    def registerFilterIndexCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerInitializedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerIsInputCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerPulseLengthCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerValueCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setFilterIndex(self, filterIndex: int) -> None: ...
    def setInitialized(self, initialized: bool) -> None: ...
    def setIsInput(self, isInput: bool) -> None: ...
    def setPulseLength(self, pulseLength: float) -> None: ...
    def setValue(self, value: bool) -> None: ...
    pass
class DifferentialDrivetrainSim():
    class KitbotGearing():
        """
        Represents a gearing option of the Toughbox mini.
        12.75:1 -- 14:50 and 14:50
        10.71:1 -- 14:50 and 16:48
        8.45:1 -- 14:50 and 19:45
        7.31:1 -- 14:50 and 21:43
        5.95:1 -- 14:50 and 24:40
        """
        def __init__(self) -> None: ...
        k10p71 = 10.71
        k12p75 = 12.75
        k5p95 = 5.95
        k7p31 = 7.31
        k8p45 = 8.45
        pass
    class KitbotMotor():
        def __init__(self) -> None: ...
        DualCIMPerSide: wpimath._controls._controls.plant.DCMotor
        DualMiniCIMPerSide: wpimath._controls._controls.plant.DCMotor
        SingleCIMPerSide: wpimath._controls._controls.plant.DCMotor
        SingleMiniCIMPerSide: wpimath._controls._controls.plant.DCMotor
        pass
    class KitbotWheelSize():
        def __init__(self) -> None: ...
        kEightInch = 0.2032
        kSixInch = 0.1524
        kTenInch = 0.254
        pass
    class State():
        def __init__(self) -> None: ...
        kHeading = 2
        kLeftPosition = 5
        kLeftVelocity = 3
        kRightPosition = 6
        kRightVelocity = 4
        kX = 0
        kY = 1
        pass
    @typing.overload
    def __init__(self, driveMotor: wpimath._controls._controls.plant.DCMotor, gearing: float, J: kilogram_square_meters, mass: kilograms, wheelRadius: meters, trackWidth: meters, measurementStdDevs: typing.List[float[7]] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]) -> None: 
        """
        Create a SimDrivetrain.

        :param drivetrainPlant: The LinearSystem representing the robot's
         drivetrain. This system can be created with
         LinearSystemId#createDrivetrainVelocitySystem or
         LinearSystemId#identifyDrivetrainSystem.

        :param trackWidth: The robot's track width.

        :param driveMotor: A {@link DCMotor} representing the left side of
         the drivetrain.

        :param gearingRatio: The gearingRatio ratio of the left side, as output
         over input. This must be the same ratio as the ratio used to identify or
         create the drivetrainPlant.

        :param wheelRadiusMeters: The radius of the wheels on the drivetrain, in
         meters.

        :param measurementStdDevs: Standard deviations for measurements, in the form
         [x, y, heading, left velocity, right velocity, left distance, right
         distance]^T. Can be omitted if no noise is desired. Gyro standard
         deviations of 0.0001 radians, velocity standard deviations of 0.05 m/s, and
         position measurement standard deviations of 0.005 meters are a reasonable
         starting point.

        Create a SimDrivetrain.

        :param driveMotor: A {@link DCMotor} representing the left side of the
         drivetrain.

        :param gearing: The gearing on the drive between motor and wheel, as
         output over input. This must be the same ratio as the ratio used to
         identify or create the drivetrainPlant.

        :param J: The moment of inertia of the drivetrain about its
         center.

        :param mass: The mass of the drivebase.

        :param wheelRadius: The radius of the wheels on the drivetrain.

        :param trackWidth: The robot's track width, or distance between left and
         right wheels.

        :param measurementStdDevs: Standard deviations for measurements, in the form
         [x, y, heading, left velocity, right velocity, left distance, right
         distance]^T. Can be omitted if no noise is desired. Gyro standard
         deviations of 0.0001 radians, velocity standard deviations of 0.05 m/s, and
         position measurement standard deviations of 0.005 meters are a reasonable
         starting point.
        """
    @typing.overload
    def __init__(self, plant: wpimath._controls._controls.system.LinearSystem_2_2_2, trackWidth: meters, driveMotor: wpimath._controls._controls.plant.DCMotor, gearingRatio: float, wheelRadius: meters, measurementStdDevs: typing.List[float[7]] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]) -> None: ...
    def clampInput(self, u: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Clamp the input vector such that no element exceeds the given voltage. If
        any does, the relative magnitudes of the input will be maintained.

        :param u: The input vector.

        :param maxVoltage: The maximum voltage.

        :returns: The normalized input.
        """
    @staticmethod
    @typing.overload
    def createKitbotSim(motor: wpimath._controls._controls.plant.DCMotor, gearing: float, wheelSize: meters, J: kilogram_square_meters, measurementStdDevs: typing.List[float[7]] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]) -> DifferentialDrivetrainSim: 
        """
        Create a sim for the standard FRC kitbot.

        :param motor: The motors installed in the bot.

        :param gearing: The gearing reduction used.

        :param wheelSize: The wheel size.

        :param measurementStdDevs: Standard deviations for measurements, in the form
         [x, y, heading, left velocity, right velocity, left distance, right
         distance]^T. Can be omitted if no noise is desired. Gyro standard
         deviations of 0.0001 radians, velocity standard deviations of 0.05 m/s, and
         position measurement standard deviations of 0.005 meters are a reasonable
         starting point.

        Create a sim for the standard FRC kitbot.

        :param motor: The motors installed in the bot.

        :param gearing: The gearing reduction used.

        :param wheelSize: The wheel size.

        :param J: The moment of inertia of the drivebase. This can be
         calculated using frc-characterization.

        :param measurementStdDevs: Standard deviations for measurements, in the form
         [x, y, heading, left velocity, right velocity, left distance, right
         distance]^T. Can be omitted if no noise is desired. Gyro standard
         deviations of 0.0001 radians, velocity standard deviations of 0.05 m/s, and
         position measurement standard deviations of 0.005 meters are a reasonable
         starting point.
        """
    @staticmethod
    @typing.overload
    def createKitbotSim(motor: wpimath._controls._controls.plant.DCMotor, gearing: float, wheelSize: meters, measurementStdDevs: typing.List[float[7]] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]) -> DifferentialDrivetrainSim: ...
    def dynamics(self, x: numpy.ndarray[numpy.float64, _Shape[7, 1]], u: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> numpy.ndarray[numpy.float64, _Shape[7, 1]]: ...
    def getCurrentDraw(self) -> amperes: 
        """
        Returns the currently drawn current.
        """
    def getGearing(self) -> float: 
        """
        Returns the current gearing reduction of the drivetrain, as output over
        input.
        """
    def getHeading(self) -> wpimath.geometry._geometry.Rotation2d: 
        """
        Returns the direction the robot is pointing.

        Note that this angle is counterclockwise-positive, while most gyros are
        clockwise positive.
        """
    def getLeftCurrentDraw(self) -> amperes: 
        """
        Returns the currently drawn current for the left side.
        """
    def getLeftPosition(self) -> meters: 
        """
        Get the left encoder position in meters.

        :returns: The encoder position.
        """
    def getLeftVelocity(self) -> meters_per_second: 
        """
        Get the left encoder velocity in meters per second.

        :returns: The encoder velocity.
        """
    def getPose(self) -> wpimath.geometry._geometry.Pose2d: 
        """
        Returns the current pose.
        """
    def getRightCurrentDraw(self) -> amperes: 
        """
        Returns the currently drawn current for the right side.
        """
    def getRightPosition(self) -> meters: 
        """
        Get the right encoder position in meters.

        :returns: The encoder position.
        """
    def getRightVelocity(self) -> meters_per_second: 
        """
        Get the right encoder velocity in meters per second.

        :returns: The encoder velocity.
        """
    def setGearing(self, newGearing: float) -> None: 
        """
        Sets the gearing reduction on the drivetrain. This is commonly used for
        shifting drivetrains.

        :param newGearing: The new gear ratio, as output over input.
        """
    def setInputs(self, leftVoltage: volts, rightVoltage: volts) -> None: 
        """
        Sets the applied voltage to the drivetrain. Note that positive voltage must
        make that side of the drivetrain travel forward (+X).

        :param leftVoltage: The left voltage.

        :param rightVoltage: The right voltage.
        """
    def setPose(self, pose: wpimath.geometry._geometry.Pose2d) -> None: 
        """
        Sets the system pose.

        :param pose: The pose.
        """
    def setState(self, state: numpy.ndarray[numpy.float64, _Shape[7, 1]]) -> None: 
        """
        Sets the system state.

        :param state: The state.
        """
    def update(self, dt: seconds) -> None: 
        """
        Updates the simulation.

        :param dt: The time that's passed since the last :meth:`.update`
         call.
        """
    pass
class DigitalPWMSim():
    """
    Class to control a simulated digital PWM output.

    This is for duty cycle PWM outputs on a DigitalOutput, not for the servo
    style PWM outputs on a PWM channel.
    """
    def __init__(self, digitalOutput: wpilib._wpilib.DigitalOutput) -> None: 
        """
        Constructs from a DigitalOutput object.

        :param digitalOutput: DigitalOutput to simulate
        """
    @staticmethod
    def createForChannel(channel: int) -> DigitalPWMSim: 
        """
        Creates an DigitalPWMSim for a digital I/O channel.

        :param channel: DIO channel

        :returns: Simulated object
                  @throws std::out_of_range if no Digital PWM is configured for that channel
        """
    @staticmethod
    def createForIndex(index: int) -> DigitalPWMSim: 
        """
        Creates an DigitalPWMSim for a simulated index.
        The index is incremented for each simulated DigitalPWM.

        :param index: simulator index

        :returns: Simulated object
        """
    def getDutyCycle(self) -> float: ...
    def getInitialized(self) -> bool: ...
    def getPin(self) -> int: ...
    def registerDutyCycleCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerInitializedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerPinCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setDutyCycle(self, dutyCycle: float) -> None: ...
    def setInitialized(self, initialized: bool) -> None: ...
    def setPin(self, pin: int) -> None: ...
    pass
class DriverStationSim():
    """
    Class to control a simulated driver station.
    """
    def __init__(self) -> None: ...
    @staticmethod
    def getAllianceStationId() -> hal._wpiHal.AllianceStationID: ...
    @staticmethod
    def getAutonomous() -> bool: ...
    @staticmethod
    def getDsAttached() -> bool: ...
    @staticmethod
    def getEStop() -> bool: ...
    @staticmethod
    def getEnabled() -> bool: ...
    @staticmethod
    def getFmsAttached() -> bool: ...
    @staticmethod
    def getJoystickOutputs(stick: int) -> int: 
        """
        Gets the joystick outputs.

        :param stick: The joystick number

        :returns: The joystick outputs
        """
    @staticmethod
    def getJoystickRumble(stick: int, rumbleNum: int) -> int: 
        """
        Gets the joystick rumble.

        :param stick: The joystick number

        :param rumbleNum: Rumble to get (0=left, 1=right)

        :returns: The joystick rumble value
        """
    @staticmethod
    def getMatchTime() -> float: ...
    @staticmethod
    def getTest() -> bool: ...
    @staticmethod
    def notifyNewData() -> None: 
        """
        Updates DriverStation data so that new values are visible to the user
        program.
        """
    @staticmethod
    def registerAllianceStationIdCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerAutonomousCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerDsAttachedCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerEStopCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerEnabledCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerFmsAttachedCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerMatchTimeCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerTestCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def resetData() -> None: ...
    @staticmethod
    def setAllianceStationId(allianceStationId: hal._wpiHal.AllianceStationID) -> None: ...
    @staticmethod
    def setAutonomous(autonomous: bool) -> None: ...
    @staticmethod
    def setDsAttached(dsAttached: bool) -> None: ...
    @staticmethod
    def setEStop(eStop: bool) -> None: ...
    @staticmethod
    def setEnabled(enabled: bool) -> None: ...
    @staticmethod
    def setEventName(name: str) -> None: 
        """
        Sets the event name.

        :param name: the event name
        """
    @staticmethod
    def setFmsAttached(fmsAttached: bool) -> None: ...
    @staticmethod
    def setGameSpecificMessage(message: str) -> None: 
        """
        Sets the game specific message.

        :param message: the game specific message
        """
    @staticmethod
    def setJoystickAxis(stick: int, axis: int, value: float) -> None: 
        """
        Gets the value of the axis on a joystick.

        :param stick: The joystick number

        :param axis: The analog axis number

        :param value: The value of the axis on the joystick
        """
    @staticmethod
    def setJoystickAxisCount(stick: int, count: int) -> None: 
        """
        Sets the number of axes for a joystick.

        :param stick: The joystick number

        :param count: The number of axes on the indicated joystick
        """
    @staticmethod
    def setJoystickAxisType(stick: int, axis: int, type: int) -> None: 
        """
        Sets the types of Axes for a joystick.

        :param stick: The joystick number

        :param axis: The target axis

        :param type: The type of axis
        """
    @staticmethod
    def setJoystickButton(stick: int, button: int, state: bool) -> None: 
        """
        Sets the state of one joystick button. Button indexes begin at 1.

        :param stick: The joystick number

        :param button: The button index, beginning at 1

        :param state: The state of the joystick button
        """
    @staticmethod
    def setJoystickButtonCount(stick: int, count: int) -> None: 
        """
        Sets the number of buttons for a joystick.

        :param stick: The joystick number

        :param count: The number of buttons on the indicated joystick
        """
    @staticmethod
    def setJoystickButtons(stick: int, buttons: int) -> None: 
        """
        Sets the state of all the buttons on a joystick.

        :param stick: The joystick number

        :param buttons: The bitmap state of the buttons on the joystick
        """
    @staticmethod
    def setJoystickIsXbox(stick: int, isXbox: bool) -> None: 
        """
        Sets the value of isXbox for a joystick.

        :param stick: The joystick number

        :param isXbox: The value of isXbox
        """
    @staticmethod
    def setJoystickName(stick: int, name: str) -> None: 
        """
        Sets the name of a joystick.

        :param stick: The joystick number

        :param name: The value of name
        """
    @staticmethod
    def setJoystickPOV(stick: int, pov: int, value: int) -> None: 
        """
        Gets the state of a POV on a joystick.

        :param stick: The joystick number

        :param pov: The POV number

        :param value: the angle of the POV in degrees, or -1 for not pressed
        """
    @staticmethod
    def setJoystickPOVCount(stick: int, count: int) -> None: 
        """
        Sets the number of POVs for a joystick.

        :param stick: The joystick number

        :param count: The number of POVs on the indicated joystick
        """
    @staticmethod
    def setJoystickType(stick: int, type: int) -> None: 
        """
        Sets the value of type for a joystick.

        :param stick: The joystick number

        :param type: The value of type
        """
    @staticmethod
    def setMatchNumber(matchNumber: int) -> None: 
        """
        Sets the match number.

        :param matchNumber: the match number
        """
    @staticmethod
    def setMatchTime(matchTime: float) -> None: ...
    @staticmethod
    def setMatchType(type: wpilib._wpilib.DriverStation.MatchType) -> None: 
        """
        Sets the match type.

        :param type: the match type
        """
    @staticmethod
    def setReplayNumber(replayNumber: int) -> None: 
        """
        Sets the replay number.

        :param replayNumber: the replay number
        """
    @staticmethod
    def setSendConsoleLine(shouldSend: bool) -> None: 
        """
        Sets suppression of DriverStation::SendConsoleLine messages.

        :param shouldSend: If false then messages will be suppressed.
        """
    @staticmethod
    def setSendError(shouldSend: bool) -> None: 
        """
        Sets suppression of DriverStation::ReportError and ReportWarning messages.

        :param shouldSend: If false then messages will be suppressed.
        """
    @staticmethod
    def setTest(test: bool) -> None: ...
    pass
class DutyCycleEncoderSim():
    """
    Class to control a simulated duty cycle encoder.
    """
    def __init__(self, encoder: wpilib._wpilib.DutyCycleEncoder) -> None: 
        """
        Constructs from a DutyCycleEncoder object.

        :param dutyCycleEncoder: DutyCycleEncoder to simulate
        """
    def set(self, turns: turns) -> None: 
        """
        Set the position tin turns.

        :param turns: The position.
        """
    def setDistance(self, distance: float) -> None: 
        """
        Set the position.
        """
    pass
class DutyCycleSim():
    """
    Class to control a simulated duty cycle digital input.
    """
    def __init__(self, dutyCycle: wpilib._wpilib.DutyCycle) -> None: 
        """
        Constructs from a DutyCycle object.

        :param dutyCycle: DutyCycle to simulate
        """
    @staticmethod
    def createForChannel(channel: int) -> DutyCycleSim: 
        """
        Creates a DutyCycleSim for a digital input channel.

        :param channel: digital input channel

        :returns: Simulated object
                  @throws std::out_of_range if no DutyCycle is configured for that channel
        """
    @staticmethod
    def createForIndex(index: int) -> DutyCycleSim: 
        """
        Creates a DutyCycleSim for a simulated index.
        The index is incremented for each simulated DutyCycle.

        :param index: simulator index

        :returns: Simulated object
        """
    def getFrequency(self) -> int: ...
    def getInitialized(self) -> bool: ...
    def getOutput(self) -> float: ...
    def registerFrequencyCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerInitializedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerOutputCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setFrequency(self, count: int) -> None: ...
    def setInitialized(self, initialized: bool) -> None: ...
    def setOutput(self, period: float) -> None: ...
    pass
class LinearSystemSim_2_1_1():
    """
    This class helps simulate linear systems. To use this class, do the following
    in the simulationPeriodic() method.

    Call the SetInput() method with the inputs to your system (generally
    voltage). Call the Update() method to update the simulation. Set simulated
    sensor readings with the simulated positions in the GetOutput() method.

    @tparam States  The number of states of the system.
    @tparam Inputs  The number of inputs to the system.
    @tparam Outputs The number of outputs of the system.
    """
    def __init__(self, system: wpimath._controls._controls.system.LinearSystem_2_1_1, measurementStdDevs: typing.List[float[1]] = [0.0]) -> None: 
        """
        Creates a simulated generic linear system.

        :param system: The system to simulate.

        :param measurementStdDevs: The standard deviations of the measurements.
        """
    def _clampInput(self, u: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Clamp the input vector such that no element exceeds the given voltage. If
        any does, the relative magnitudes of the input will be maintained.

        :param u: The input vector.

        :returns: The normalized input.
        """
    def _updateX(self, currentXhat: numpy.ndarray[numpy.float64, _Shape[2, 1]], u: numpy.ndarray[numpy.float64, _Shape[1, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Updates the state estimate of the system.

        :param currentXhat: The current state estimate.

        :param u: The system inputs (usually voltage).

        :param dt: The time difference between controller updates.
        """
    def getCurrentDraw(self) -> amperes: 
        """
        Returns the current drawn by this simulated system. Override this method to
        add a custom current calculation.

        :returns: The current drawn by this simulated mechanism.
        """
    @typing.overload
    def getOutput(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the current output of the plant.

        :returns: The current output of the plant.

        Returns an element of the current output of the plant.

        :param row: The row to return.

        :returns: An element of the current output of the plant.
        """
    @typing.overload
    def getOutput(self, row: int) -> float: ...
    @typing.overload
    def setInput(self, row: int, value: float) -> None: 
        """
        Sets the system inputs (usually voltages).

        :param u: The system inputs.
        """
    @typing.overload
    def setInput(self, u: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> None: ...
    def setState(self, state: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: 
        """
        Sets the system state.

        :param state: The new state.
        """
    def update(self, dt: seconds) -> None: 
        """
        Updates the simulation.

        :param dt: The time between updates.
        """
    @property
    def _m_measurementStdDevs(self) -> typing.List[float[1]]:
        """
        :type: typing.List[float[1]]
        """
    @property
    def _m_plant(self) -> wpimath._controls._controls.system.LinearSystem_2_1_1:
        """
        :type: wpimath._controls._controls.system.LinearSystem_2_1_1
        """
    @property
    def _m_u(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[1, 1]]
        """
    @property
    def _m_x(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[2, 1]]
        """
    @property
    def _m_y(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[1, 1]]
        """
    pass
class EncoderSim():
    """
    Class to control a simulated encoder.
    """
    def __init__(self, encoder: wpilib._wpilib.Encoder) -> None: 
        """
        Constructs from an Encoder object.

        :param encoder: Encoder to simulate
        """
    @staticmethod
    def createForChannel(channel: int) -> EncoderSim: 
        """
        Creates an EncoderSim for a digital input channel.  Encoders take two
        channels, so either one may be specified.

        :param channel: digital input channel

        :returns: Simulated object
                  @throws NoSuchElementException if no Encoder is configured for that channel
        """
    @staticmethod
    def createForIndex(index: int) -> EncoderSim: 
        """
        Creates an EncoderSim for a simulated index.
        The index is incremented for each simulated Encoder.

        :param index: simulator index

        :returns: Simulated object
        """
    def getCount(self) -> int: ...
    def getDirection(self) -> bool: ...
    def getDistance(self) -> float: ...
    def getDistancePerPulse(self) -> float: ...
    def getInitialized(self) -> bool: ...
    def getMaxPeriod(self) -> float: ...
    def getPeriod(self) -> float: ...
    def getRate(self) -> float: ...
    def getReset(self) -> bool: ...
    def getReverseDirection(self) -> bool: ...
    def getSamplesToAverage(self) -> int: ...
    def registerCountCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerDirectionCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerDistancePerPulseCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerInitializedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerMaxPeriodCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerPeriodCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerResetCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerReverseDirectionCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerSamplesToAverageCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setCount(self, count: int) -> None: ...
    def setDirection(self, direction: bool) -> None: ...
    def setDistance(self, distance: float) -> None: ...
    def setDistancePerPulse(self, distancePerPulse: float) -> None: ...
    def setInitialized(self, initialized: bool) -> None: ...
    def setMaxPeriod(self, maxPeriod: float) -> None: ...
    def setPeriod(self, period: float) -> None: ...
    def setRate(self, rate: float) -> None: ...
    def setReset(self, reset: bool) -> None: ...
    def setReverseDirection(self, reverseDirection: bool) -> None: ...
    def setSamplesToAverage(self, samplesToAverage: int) -> None: ...
    pass
class LinearSystemSim_1_1_1():
    """
    This class helps simulate linear systems. To use this class, do the following
    in the simulationPeriodic() method.

    Call the SetInput() method with the inputs to your system (generally
    voltage). Call the Update() method to update the simulation. Set simulated
    sensor readings with the simulated positions in the GetOutput() method.

    @tparam States  The number of states of the system.
    @tparam Inputs  The number of inputs to the system.
    @tparam Outputs The number of outputs of the system.
    """
    def __init__(self, system: wpimath._controls._controls.system.LinearSystem_1_1_1, measurementStdDevs: typing.List[float[1]] = [0.0]) -> None: 
        """
        Creates a simulated generic linear system.

        :param system: The system to simulate.

        :param measurementStdDevs: The standard deviations of the measurements.
        """
    def _clampInput(self, u: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Clamp the input vector such that no element exceeds the given voltage. If
        any does, the relative magnitudes of the input will be maintained.

        :param u: The input vector.

        :returns: The normalized input.
        """
    def _updateX(self, currentXhat: numpy.ndarray[numpy.float64, _Shape[1, 1]], u: numpy.ndarray[numpy.float64, _Shape[1, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Updates the state estimate of the system.

        :param currentXhat: The current state estimate.

        :param u: The system inputs (usually voltage).

        :param dt: The time difference between controller updates.
        """
    def getCurrentDraw(self) -> amperes: 
        """
        Returns the current drawn by this simulated system. Override this method to
        add a custom current calculation.

        :returns: The current drawn by this simulated mechanism.
        """
    @typing.overload
    def getOutput(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the current output of the plant.

        :returns: The current output of the plant.

        Returns an element of the current output of the plant.

        :param row: The row to return.

        :returns: An element of the current output of the plant.
        """
    @typing.overload
    def getOutput(self, row: int) -> float: ...
    @typing.overload
    def setInput(self, row: int, value: float) -> None: 
        """
        Sets the system inputs (usually voltages).

        :param u: The system inputs.
        """
    @typing.overload
    def setInput(self, u: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> None: ...
    def setState(self, state: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> None: 
        """
        Sets the system state.

        :param state: The new state.
        """
    def update(self, dt: seconds) -> None: 
        """
        Updates the simulation.

        :param dt: The time between updates.
        """
    @property
    def _m_measurementStdDevs(self) -> typing.List[float[1]]:
        """
        :type: typing.List[float[1]]
        """
    @property
    def _m_plant(self) -> wpimath._controls._controls.system.LinearSystem_1_1_1:
        """
        :type: wpimath._controls._controls.system.LinearSystem_1_1_1
        """
    @property
    def _m_u(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[1, 1]]
        """
    @property
    def _m_x(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[1, 1]]
        """
    @property
    def _m_y(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[1, 1]]
        """
    pass
class GenericHIDSim():
    """
    Class to control a simulated generic joystick.
    """
    @typing.overload
    def __init__(self, joystick: wpilib.interfaces._interfaces.GenericHID) -> None: 
        """
        Constructs from a GenericHID object.

        :param joystick: joystick to simulate

        Constructs from a joystick port number.

        :param port: port number
        """
    @typing.overload
    def __init__(self, port: int) -> None: ...
    def getOutput(self, outputNumber: int) -> bool: ...
    def getOutputs(self) -> int: ...
    def getRumble(self, type: wpilib.interfaces._interfaces.GenericHID.RumbleType) -> float: ...
    def notifyNewData(self) -> None: 
        """
        Updates joystick data so that new values are visible to the user program.
        """
    def setAxisCount(self, count: int) -> None: ...
    def setAxisType(self, axis: int, type: int) -> None: ...
    def setButtonCount(self, count: int) -> None: ...
    def setName(self, name: str) -> None: ...
    @typing.overload
    def setPOV(self, pov: int, value: int) -> None: ...
    @typing.overload
    def setPOV(self, value: int) -> None: ...
    def setPOVCount(self, count: int) -> None: ...
    def setRawAxis(self, axis: int, value: float) -> None: ...
    def setRawButton(self, button: int, value: bool) -> None: ...
    def setType(self, type: wpilib.interfaces._interfaces.GenericHID.HIDType) -> None: ...
    pass
class JoystickSim(GenericHIDSim):
    """
    Class to control a simulated joystick.
    """
    @typing.overload
    def __init__(self, joystick: wpilib._wpilib.Joystick) -> None: 
        """
        Constructs from a Joystick object.

        :param joystick: joystick to simulate

        Constructs from a joystick port number.

        :param port: port number
        """
    @typing.overload
    def __init__(self, port: int) -> None: ...
    def setThrottle(self, value: float) -> None: ...
    def setTop(self, state: bool) -> None: ...
    def setTrigger(self, state: bool) -> None: ...
    def setTwist(self, value: float) -> None: ...
    def setX(self, value: float) -> None: ...
    def setY(self, value: float) -> None: ...
    def setZ(self, value: float) -> None: ...
    pass
class FlywheelSim(LinearSystemSim_1_1_1):
    """
    Represents a simulated flywheel mechanism.
    """
    @typing.overload
    def __init__(self, gearbox: wpimath._controls._controls.plant.DCMotor, gearing: float, moi: kilogram_square_meters, measurementStdDevs: typing.List[float[1]] = [0.0]) -> None: 
        """
        Creates a simulated flywhel mechanism.

        :param plant: The linear system representing the flywheel.

        :param gearbox: The type of and number of motors in the flywheel
         gearbox.

        :param gearing: The gearing of the flywheel (numbers greater than
         1 represent reductions).

        :param measurementStdDevs: The standard deviation of the measurement noise.

        Creates a simulated flywhel mechanism.

        :param gearbox: The type of and number of motors in the flywheel
         gearbox.

        :param gearing: The gearing of the flywheel (numbers greater than
         1 represent reductions).

        :param moi: The moment of inertia of the flywheel.

        :param measurementStdDevs: The standard deviation of the measurement noise.
        """
    @typing.overload
    def __init__(self, plant: wpimath._controls._controls.system.LinearSystem_1_1_1, gearbox: wpimath._controls._controls.plant.DCMotor, gearing: float, measurementStdDevs: typing.List[float[1]] = [0.0]) -> None: ...
    def getAngularVelocity(self) -> radians_per_second: 
        """
        Returns the flywheel velocity.

        :returns: The flywheel velocity.
        """
    def getCurrentDraw(self) -> amperes: 
        """
        Returns the flywheel current draw.

        :returns: The flywheel current draw.
        """
    def setInputVoltage(self, voltage: volts) -> None: 
        """
        Sets the input voltage for the flywheel.

        :param voltage: The input voltage.
        """
    pass
class LinearSystemSim_1_1_2():
    """
    This class helps simulate linear systems. To use this class, do the following
    in the simulationPeriodic() method.

    Call the SetInput() method with the inputs to your system (generally
    voltage). Call the Update() method to update the simulation. Set simulated
    sensor readings with the simulated positions in the GetOutput() method.

    @tparam States  The number of states of the system.
    @tparam Inputs  The number of inputs to the system.
    @tparam Outputs The number of outputs of the system.
    """
    def __init__(self, system: wpimath._controls._controls.system.LinearSystem_1_1_2, measurementStdDevs: typing.List[float[2]] = [0.0, 0.0]) -> None: 
        """
        Creates a simulated generic linear system.

        :param system: The system to simulate.

        :param measurementStdDevs: The standard deviations of the measurements.
        """
    def _clampInput(self, u: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Clamp the input vector such that no element exceeds the given voltage. If
        any does, the relative magnitudes of the input will be maintained.

        :param u: The input vector.

        :returns: The normalized input.
        """
    def _updateX(self, currentXhat: numpy.ndarray[numpy.float64, _Shape[1, 1]], u: numpy.ndarray[numpy.float64, _Shape[1, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Updates the state estimate of the system.

        :param currentXhat: The current state estimate.

        :param u: The system inputs (usually voltage).

        :param dt: The time difference between controller updates.
        """
    def getCurrentDraw(self) -> amperes: 
        """
        Returns the current drawn by this simulated system. Override this method to
        add a custom current calculation.

        :returns: The current drawn by this simulated mechanism.
        """
    @typing.overload
    def getOutput(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns the current output of the plant.

        :returns: The current output of the plant.

        Returns an element of the current output of the plant.

        :param row: The row to return.

        :returns: An element of the current output of the plant.
        """
    @typing.overload
    def getOutput(self, row: int) -> float: ...
    @typing.overload
    def setInput(self, row: int, value: float) -> None: 
        """
        Sets the system inputs (usually voltages).

        :param u: The system inputs.
        """
    @typing.overload
    def setInput(self, u: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> None: ...
    def setState(self, state: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> None: 
        """
        Sets the system state.

        :param state: The new state.
        """
    def update(self, dt: seconds) -> None: 
        """
        Updates the simulation.

        :param dt: The time between updates.
        """
    @property
    def _m_measurementStdDevs(self) -> typing.List[float[2]]:
        """
        :type: typing.List[float[2]]
        """
    @property
    def _m_plant(self) -> wpimath._controls._controls.system.LinearSystem_1_1_2:
        """
        :type: wpimath._controls._controls.system.LinearSystem_1_1_2
        """
    @property
    def _m_u(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[1, 1]]
        """
    @property
    def _m_x(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[1, 1]]
        """
    @property
    def _m_y(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[2, 1]]
        """
    pass
class ElevatorSim(LinearSystemSim_2_1_1):
    """
    Represents a simulated elevator mechanism.
    """
    @typing.overload
    def __init__(self, gearbox: wpimath._controls._controls.plant.DCMotor, gearing: float, carriageMass: kilograms, drumRadius: meters, minHeight: meters, maxHeight: meters, measurementStdDevs: typing.List[float[1]] = [0.0]) -> None: 
        """
        Constructs a simulated elevator mechanism.

        :param plant: The linear system that represents the elevator.

        :param gearbox: The type of and number of motors in your
         elevator gearbox.

        :param gearing: The gearing of the elevator (numbers greater
         than 1 represent reductions).

        :param drumRadius: The radius of the drum that your cable is
         wrapped around.

        :param minHeight: The minimum allowed height of the elevator.

        :param maxHeight: The maximum allowed height of the elevator.

        :param measurementStdDevs: The standard deviation of the measurements.

        Constructs a simulated elevator mechanism.

        :param gearbox: The type of and number of motors in your
         elevator gearbox.

        :param gearing: The gearing of the elevator (numbers greater
         than 1 represent reductions).

        :param carriageMass: The mass of the elevator carriage.

        :param drumRadius: The radius of the drum that your cable is
         wrapped around.

        :param minHeight: The minimum allowed height of the elevator.

        :param maxHeight: The maximum allowed height of the elevator.

        :param measurementStdDevs: The standard deviation of the measurements.
        """
    @typing.overload
    def __init__(self, plant: wpimath._controls._controls.system.LinearSystem_2_1_1, gearbox: wpimath._controls._controls.plant.DCMotor, gearing: float, drumRadius: meters, minHeight: meters, maxHeight: meters, measurementStdDevs: typing.List[float[1]] = [0.0]) -> None: ...
    def _updateX(self, currentXhat: numpy.ndarray[numpy.float64, _Shape[2, 1]], u: numpy.ndarray[numpy.float64, _Shape[1, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Updates the state estimate of the elevator.

        :param currentXhat: The current state estimate.

        :param u: The system inputs (voltage).

        :param dt: The time difference between controller updates.
        """
    def getCurrentDraw(self) -> amperes: 
        """
        Returns the elevator current draw.

        :returns: The elevator current draw.
        """
    def getPosition(self) -> meters: 
        """
        Returns the position of the elevator.

        :returns: The position of the elevator.
        """
    def getVelocity(self) -> meters_per_second: 
        """
        Returns the velocity of the elevator.

        :returns: The velocity of the elevator.
        """
    def hasHitLowerLimit(self, x: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> bool: 
        """
        Returns whether the elevator has hit the lower limit.

        :param x: The current elevator state.

        :returns: Whether the elevator has hit the lower limit.
        """
    def hasHitUpperLimit(self, x: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> bool: 
        """
        Returns whether the elevator has hit the upper limit.

        :param x: The current elevator state.

        :returns: Whether the elevator has hit the upper limit.
        """
    def setInputVoltage(self, voltage: volts) -> None: 
        """
        Sets the input voltage for the elevator.

        :param voltage: The input voltage.
        """
    pass
class LinearSystemSim_2_1_2():
    """
    This class helps simulate linear systems. To use this class, do the following
    in the simulationPeriodic() method.

    Call the SetInput() method with the inputs to your system (generally
    voltage). Call the Update() method to update the simulation. Set simulated
    sensor readings with the simulated positions in the GetOutput() method.

    @tparam States  The number of states of the system.
    @tparam Inputs  The number of inputs to the system.
    @tparam Outputs The number of outputs of the system.
    """
    def __init__(self, system: wpimath._controls._controls.system.LinearSystem_2_1_2, measurementStdDevs: typing.List[float[2]] = [0.0, 0.0]) -> None: 
        """
        Creates a simulated generic linear system.

        :param system: The system to simulate.

        :param measurementStdDevs: The standard deviations of the measurements.
        """
    def _clampInput(self, u: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Clamp the input vector such that no element exceeds the given voltage. If
        any does, the relative magnitudes of the input will be maintained.

        :param u: The input vector.

        :returns: The normalized input.
        """
    def _updateX(self, currentXhat: numpy.ndarray[numpy.float64, _Shape[2, 1]], u: numpy.ndarray[numpy.float64, _Shape[1, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Updates the state estimate of the system.

        :param currentXhat: The current state estimate.

        :param u: The system inputs (usually voltage).

        :param dt: The time difference between controller updates.
        """
    def getCurrentDraw(self) -> amperes: 
        """
        Returns the current drawn by this simulated system. Override this method to
        add a custom current calculation.

        :returns: The current drawn by this simulated mechanism.
        """
    @typing.overload
    def getOutput(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns the current output of the plant.

        :returns: The current output of the plant.

        Returns an element of the current output of the plant.

        :param row: The row to return.

        :returns: An element of the current output of the plant.
        """
    @typing.overload
    def getOutput(self, row: int) -> float: ...
    @typing.overload
    def setInput(self, row: int, value: float) -> None: 
        """
        Sets the system inputs (usually voltages).

        :param u: The system inputs.
        """
    @typing.overload
    def setInput(self, u: numpy.ndarray[numpy.float64, _Shape[1, 1]]) -> None: ...
    def setState(self, state: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: 
        """
        Sets the system state.

        :param state: The new state.
        """
    def update(self, dt: seconds) -> None: 
        """
        Updates the simulation.

        :param dt: The time between updates.
        """
    @property
    def _m_measurementStdDevs(self) -> typing.List[float[2]]:
        """
        :type: typing.List[float[2]]
        """
    @property
    def _m_plant(self) -> wpimath._controls._controls.system.LinearSystem_2_1_2:
        """
        :type: wpimath._controls._controls.system.LinearSystem_2_1_2
        """
    @property
    def _m_u(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[1, 1]]
        """
    @property
    def _m_x(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[2, 1]]
        """
    @property
    def _m_y(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[2, 1]]
        """
    pass
class LinearSystemSim_2_2_1():
    """
    This class helps simulate linear systems. To use this class, do the following
    in the simulationPeriodic() method.

    Call the SetInput() method with the inputs to your system (generally
    voltage). Call the Update() method to update the simulation. Set simulated
    sensor readings with the simulated positions in the GetOutput() method.

    @tparam States  The number of states of the system.
    @tparam Inputs  The number of inputs to the system.
    @tparam Outputs The number of outputs of the system.
    """
    def __init__(self, system: wpimath._controls._controls.system.LinearSystem_2_2_1, measurementStdDevs: typing.List[float[1]] = [0.0]) -> None: 
        """
        Creates a simulated generic linear system.

        :param system: The system to simulate.

        :param measurementStdDevs: The standard deviations of the measurements.
        """
    def _clampInput(self, u: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Clamp the input vector such that no element exceeds the given voltage. If
        any does, the relative magnitudes of the input will be maintained.

        :param u: The input vector.

        :returns: The normalized input.
        """
    def _updateX(self, currentXhat: numpy.ndarray[numpy.float64, _Shape[2, 1]], u: numpy.ndarray[numpy.float64, _Shape[2, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Updates the state estimate of the system.

        :param currentXhat: The current state estimate.

        :param u: The system inputs (usually voltage).

        :param dt: The time difference between controller updates.
        """
    def getCurrentDraw(self) -> amperes: 
        """
        Returns the current drawn by this simulated system. Override this method to
        add a custom current calculation.

        :returns: The current drawn by this simulated mechanism.
        """
    @typing.overload
    def getOutput(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]: 
        """
        Returns the current output of the plant.

        :returns: The current output of the plant.

        Returns an element of the current output of the plant.

        :param row: The row to return.

        :returns: An element of the current output of the plant.
        """
    @typing.overload
    def getOutput(self, row: int) -> float: ...
    @typing.overload
    def setInput(self, row: int, value: float) -> None: 
        """
        Sets the system inputs (usually voltages).

        :param u: The system inputs.
        """
    @typing.overload
    def setInput(self, u: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: ...
    def setState(self, state: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: 
        """
        Sets the system state.

        :param state: The new state.
        """
    def update(self, dt: seconds) -> None: 
        """
        Updates the simulation.

        :param dt: The time between updates.
        """
    @property
    def _m_measurementStdDevs(self) -> typing.List[float[1]]:
        """
        :type: typing.List[float[1]]
        """
    @property
    def _m_plant(self) -> wpimath._controls._controls.system.LinearSystem_2_2_1:
        """
        :type: wpimath._controls._controls.system.LinearSystem_2_2_1
        """
    @property
    def _m_u(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[2, 1]]
        """
    @property
    def _m_x(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[2, 1]]
        """
    @property
    def _m_y(self) -> numpy.ndarray[numpy.float64, _Shape[1, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[1, 1]]
        """
    pass
class LinearSystemSim_2_2_2():
    """
    This class helps simulate linear systems. To use this class, do the following
    in the simulationPeriodic() method.

    Call the SetInput() method with the inputs to your system (generally
    voltage). Call the Update() method to update the simulation. Set simulated
    sensor readings with the simulated positions in the GetOutput() method.

    @tparam States  The number of states of the system.
    @tparam Inputs  The number of inputs to the system.
    @tparam Outputs The number of outputs of the system.
    """
    def __init__(self, system: wpimath._controls._controls.system.LinearSystem_2_2_2, measurementStdDevs: typing.List[float[2]] = [0.0, 0.0]) -> None: 
        """
        Creates a simulated generic linear system.

        :param system: The system to simulate.

        :param measurementStdDevs: The standard deviations of the measurements.
        """
    def _clampInput(self, u: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Clamp the input vector such that no element exceeds the given voltage. If
        any does, the relative magnitudes of the input will be maintained.

        :param u: The input vector.

        :returns: The normalized input.
        """
    def _updateX(self, currentXhat: numpy.ndarray[numpy.float64, _Shape[2, 1]], u: numpy.ndarray[numpy.float64, _Shape[2, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Updates the state estimate of the system.

        :param currentXhat: The current state estimate.

        :param u: The system inputs (usually voltage).

        :param dt: The time difference between controller updates.
        """
    def getCurrentDraw(self) -> amperes: 
        """
        Returns the current drawn by this simulated system. Override this method to
        add a custom current calculation.

        :returns: The current drawn by this simulated mechanism.
        """
    @typing.overload
    def getOutput(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Returns the current output of the plant.

        :returns: The current output of the plant.

        Returns an element of the current output of the plant.

        :param row: The row to return.

        :returns: An element of the current output of the plant.
        """
    @typing.overload
    def getOutput(self, row: int) -> float: ...
    @typing.overload
    def setInput(self, row: int, value: float) -> None: 
        """
        Sets the system inputs (usually voltages).

        :param u: The system inputs.
        """
    @typing.overload
    def setInput(self, u: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: ...
    def setState(self, state: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> None: 
        """
        Sets the system state.

        :param state: The new state.
        """
    def update(self, dt: seconds) -> None: 
        """
        Updates the simulation.

        :param dt: The time between updates.
        """
    @property
    def _m_measurementStdDevs(self) -> typing.List[float[2]]:
        """
        :type: typing.List[float[2]]
        """
    @property
    def _m_plant(self) -> wpimath._controls._controls.system.LinearSystem_2_2_2:
        """
        :type: wpimath._controls._controls.system.LinearSystem_2_2_2
        """
    @property
    def _m_u(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[2, 1]]
        """
    @property
    def _m_x(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[2, 1]]
        """
    @property
    def _m_y(self) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[2, 1]]
        """
    pass
class Mechanism2D():
    def __init__(self) -> None: ...
    def setLigamentAngle(self, ligamentPath: str, angle: float) -> None: 
        """
        Set/Create the angle of a ligament

        :param ligamentPath: json path to the ligament

        :param angle: to set the ligament
        """
    def setLigamentLength(self, ligamentPath: str, length: float) -> None: 
        """
        Set/Create the length of a ligament

        :param ligamentPath: json path to the ligament

        :param length: to set the ligament
        """
    pass
class PCMSim():
    """
    Class to control a simulated Pneumatic Control Module (PCM).
    """
    @typing.overload
    def __init__(self) -> None: 
        """
        Constructs with the default PCM module number (CAN ID).

        Constructs from a PCM module number (CAN ID).

        :param module: module number

        Constructs from a Compressor object.

        :param compressor: Compressor connected to PCM to simulate
        """
    @typing.overload
    def __init__(self, compressor: wpilib._wpilib.Compressor) -> None: ...
    @typing.overload
    def __init__(self, module: int) -> None: ...
    def getAllSolenoidOutputs(self) -> int: ...
    def getClosedLoopEnabled(self) -> bool: ...
    def getCompressorCurrent(self) -> float: ...
    def getCompressorInitialized(self) -> bool: ...
    def getCompressorOn(self) -> bool: ...
    def getPressureSwitch(self) -> bool: ...
    def getSolenoidInitialized(self, channel: int) -> bool: ...
    def getSolenoidOutput(self, channel: int) -> bool: ...
    def registerClosedLoopEnabledCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerCompressorCurrentCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerCompressorInitializedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerCompressorOnCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerPressureSwitchCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerSolenoidInitializedCallback(self, channel: int, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerSolenoidOutputCallback(self, channel: int, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setAllSolenoidOutputs(self, outputs: int) -> None: ...
    def setClosedLoopEnabled(self, closedLoopEnabled: bool) -> None: ...
    def setCompressorCurrent(self, compressorCurrent: float) -> None: ...
    def setCompressorInitialized(self, compressorInitialized: bool) -> None: ...
    def setCompressorOn(self, compressorOn: bool) -> None: ...
    def setPressureSwitch(self, pressureSwitch: bool) -> None: ...
    def setSolenoidInitialized(self, channel: int, solenoidInitialized: bool) -> None: ...
    def setSolenoidOutput(self, channel: int, solenoidOutput: bool) -> None: ...
    pass
class PDPSim():
    """
    Class to control a simulated Power Distribution Panel (PDP).
    """
    @typing.overload
    def __init__(self, module: int = 0) -> None: 
        """
        Constructs from a PDP module number (CAN ID).

        :param module: module number

        Constructs from a PowerDistributionPanel object.

        :param pdp: PowerDistributionPanel to simulate
        """
    @typing.overload
    def __init__(self, pdp: wpilib._wpilib.PowerDistributionPanel) -> None: ...
    def getAllCurrents(self) -> float: ...
    def getCurrent(self, channel: int) -> float: ...
    def getInitialized(self) -> bool: ...
    def getTemperature(self) -> float: ...
    def getVoltage(self) -> float: ...
    def registerCurrentCallback(self, channel: int, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerInitializedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerTemperatureCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerVoltageCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setAllCurrents(self, currents: float) -> None: ...
    def setCurrent(self, channel: int, current: float) -> None: ...
    def setInitialized(self, initialized: bool) -> None: ...
    def setTemperature(self, temperature: float) -> None: ...
    def setVoltage(self, voltage: float) -> None: ...
    pass
class PWMSim():
    """
    Class to control a simulated PWM output.
    """
    @typing.overload
    def __init__(self, channel: int) -> None: 
        """
        Constructs from a PWM object.

        :param pwm: PWM to simulate

        Constructs from a PWM channel number.

        :param channel: Channel number
        """
    @typing.overload
    def __init__(self, pwm: wpilib._wpilib.PWM) -> None: ...
    def getInitialized(self) -> bool: ...
    def getPeriodScale(self) -> int: ...
    def getPosition(self) -> float: ...
    def getRawValue(self) -> int: ...
    def getSpeed(self) -> float: ...
    def getZeroLatch(self) -> bool: ...
    def registerInitializedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerPeriodScaleCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerPositionCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerRawValueCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerSpeedCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerZeroLatchCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setInitialized(self, initialized: bool) -> None: ...
    def setPeriodScale(self, periodScale: int) -> None: ...
    def setPosition(self, position: float) -> None: ...
    def setRawValue(self, rawValue: int) -> None: ...
    def setSpeed(self, speed: float) -> None: ...
    def setZeroLatch(self, zeroLatch: bool) -> None: ...
    pass
class RelaySim():
    """
    Class to control a simulated relay.
    """
    @typing.overload
    def __init__(self, channel: int) -> None: 
        """
        Constructs from a Relay object.

        :param relay: Relay to simulate

        Constructs from a relay channel number.

        :param channel: Channel number
        """
    @typing.overload
    def __init__(self, relay: wpilib._wpilib.Relay) -> None: ...
    def getForward(self) -> bool: ...
    def getInitializedForward(self) -> bool: ...
    def getInitializedReverse(self) -> bool: ...
    def getReverse(self) -> bool: ...
    def registerForwardCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerInitializedForwardCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerInitializedReverseCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerReverseCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setForward(self, forward: bool) -> None: ...
    def setInitializedForward(self, initializedForward: bool) -> None: ...
    def setInitializedReverse(self, initializedReverse: bool) -> None: ...
    def setReverse(self, reverse: bool) -> None: ...
    pass
class RoboRioSim():
    """
    Class to control a simulated RoboRIO.
    """
    def __init__(self) -> None: ...
    @staticmethod
    def getFPGAButton() -> bool: ...
    @staticmethod
    def getUserActive3V3() -> bool: ...
    @staticmethod
    def getUserActive5V() -> bool: ...
    @staticmethod
    def getUserActive6V() -> bool: ...
    @staticmethod
    def getUserCurrent3V3() -> amperes: ...
    @staticmethod
    def getUserCurrent5V() -> amperes: ...
    @staticmethod
    def getUserCurrent6V() -> amperes: ...
    @staticmethod
    def getUserFaults3V3() -> int: ...
    @staticmethod
    def getUserFaults5V() -> int: ...
    @staticmethod
    def getUserFaults6V() -> int: ...
    @staticmethod
    def getUserVoltage3V3() -> volts: ...
    @staticmethod
    def getUserVoltage5V() -> volts: ...
    @staticmethod
    def getUserVoltage6V() -> volts: ...
    @staticmethod
    def getVInCurrent() -> amperes: ...
    @staticmethod
    def getVInVoltage() -> volts: ...
    @staticmethod
    def registerFPGAButtonCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerUserActive3V3Callback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerUserActive5VCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerUserActive6VCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerUserCurrent3V3Callback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerUserCurrent5VCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerUserCurrent6VCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerUserFaults3V3Callback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerUserFaults5VCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerUserFaults6VCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerUserVoltage3V3Callback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerUserVoltage5VCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerUserVoltage6VCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerVInCurrentCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def registerVInVoltageCallback(callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    @staticmethod
    def setFPGAButton(fPGAButton: bool) -> None: ...
    @staticmethod
    def setUserActive3V3(userActive3V3: bool) -> None: ...
    @staticmethod
    def setUserActive5V(userActive5V: bool) -> None: ...
    @staticmethod
    def setUserActive6V(userActive6V: bool) -> None: ...
    @staticmethod
    def setUserCurrent3V3(userCurrent3V3: amperes) -> None: ...
    @staticmethod
    def setUserCurrent5V(userCurrent5V: amperes) -> None: ...
    @staticmethod
    def setUserCurrent6V(userCurrent6V: amperes) -> None: ...
    @staticmethod
    def setUserFaults3V3(userFaults3V3: int) -> None: ...
    @staticmethod
    def setUserFaults5V(userFaults5V: int) -> None: ...
    @staticmethod
    def setUserFaults6V(userFaults6V: int) -> None: ...
    @staticmethod
    def setUserVoltage3V3(userVoltage3V3: volts) -> None: ...
    @staticmethod
    def setUserVoltage5V(userVoltage5V: volts) -> None: ...
    @staticmethod
    def setUserVoltage6V(userVoltage6V: volts) -> None: ...
    @staticmethod
    def setVInCurrent(vInCurrent: amperes) -> None: ...
    @staticmethod
    def setVInVoltage(vInVoltage: volts) -> None: ...
    pass
class SPIAccelerometerSim():
    def __init__(self, index: int) -> None: ...
    def getActive(self) -> bool: ...
    def getRange(self) -> int: ...
    def getX(self) -> float: ...
    def getY(self) -> float: ...
    def getZ(self) -> float: ...
    def registerActiveCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerRangeCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerXCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerYCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def registerZCallback(self, callback: typing.Callable[[str, HAL_Value], None], initialNotify: bool) -> CallbackStore: ...
    def resetData(self) -> None: ...
    def setActive(self, active: bool) -> None: ...
    def setRange(self, range: int) -> None: ...
    def setX(self, x: float) -> None: ...
    def setY(self, y: float) -> None: ...
    def setZ(self, z: float) -> None: ...
    pass
class SimDeviceSim():
    """
    Interact with a generic simulated device

    Any devices that support simulation but don't have a dedicated sim
    object associated with it can be interacted with via this object.
    You just need to know the name of the associated object.

    Here are two ways to find the names of available devices:

    * The static function :meth:`.enumerateDevices` can give you a list of
      all available devices -- note that the device must be created first
      before this will return any results!
    * When running the WPILib simulation GUI, the names of the 'Other Devices'
      panel are names of devices that you can interact with via this class.

    Once you've created a simulated device, you can use the :meth:`.enumerateValues`
    method to determine what values you can interact with.


    .. note:: WPILib has simulation support for all of its devices. Some
              vendors may only have limited support for simulation -- read
              the vendor's documentation or contact them for more information.
    """
    def __init__(self, name: str) -> None: 
        """
        Constructs a SimDeviceSim.

        :param name: name of the SimDevice
        """
    @staticmethod
    def enumerateDevices(prefix: str = '') -> typing.List[str]: 
        """
        Returns a list of available device names
        """
    def enumerateValues(self) -> typing.List[typing.Tuple[str, bool]]: 
        """
        Returns a list of (name, readonly) tuples of available values for this device
        """
    def getBoolean(self, name: str) -> hal._wpiHal.SimBoolean: 
        """
        Retrieves an object that allows you to interact with simulated values
        represented as a boolean.
        """
    def getDouble(self, name: str) -> hal._wpiHal.SimDouble: 
        """
        Retrieves an object that allows you to interact with simulated values
        represented as a double.
        """
    def getEnum(self, name: str) -> hal._wpiHal.SimEnum: ...
    @staticmethod
    def getEnumOptions(val: hal._wpiHal.SimEnum) -> typing.List[str]: ...
    def getValue(self, name: str) -> hal._wpiHal.SimValue: 
        """
        Provides a readonly mechanism to retrieve all types of device values
        """
    @staticmethod
    def resetData() -> None: ...
    pass
class SingleJointedArmSim(LinearSystemSim_2_1_1):
    """
    Represents a simulated arm mechanism.
    """
    @typing.overload
    def __init__(self, gearbox: wpimath._controls._controls.plant.DCMotor, gearing: float, moi: kilogram_square_meters, armLength: meters, minAngle: radians, maxAngle: radians, mass: kilograms, simulateGravity: bool, measurementStdDevs: typing.List[float[1]] = [0.0]) -> None: 
        """
        Creates a simulated arm mechanism.

        :param system: The system representing this arm.

        :param gearbox: The type and number of motors on the arm gearbox.

        :param gearing: The gear ratio of the arm (numbers greater than 1
         represent reductions).

        :param armLength: The length of the arm.

        :param minAngle: The minimum angle that the arm is capable of.

        :param maxAngle: The maximum angle that the arm is capable of.

        :param mass: The mass of the arm.

        :param measurementStdDevs: The standard deviations of the measurements.

        :param simulateGravity: Whether gravity should be simulated or not.

        Creates a simulated arm mechanism.

        :param gearbox: The type and number of motors on the arm gearbox.

        :param gearing: The gear ratio of the arm (numbers greater than 1
         represent reductions).

        :param moi: The moment of inertia of the arm. This can be
         calculated from CAD software.

        :param armLength: The length of the arm.

        :param minAngle: The minimum angle that the arm is capable of.

        :param maxAngle: The maximum angle that the arm is capable of.

        :param mass: The mass of the arm.

        :param measurementStdDevs: The standard deviation of the measurement noise.

        :param simulateGravity: Whether gravity should be simulated or not.
        """
    @typing.overload
    def __init__(self, system: wpimath._controls._controls.system.LinearSystem_2_1_1, gearbox: wpimath._controls._controls.plant.DCMotor, gearing: float, armLength: meters, minAngle: radians, maxAngle: radians, mass: kilograms, simulateGravity: bool, measurementStdDevs: typing.List[float[1]] = [0.0]) -> None: ...
    def _updateX(self, currentXhat: numpy.ndarray[numpy.float64, _Shape[2, 1]], u: numpy.ndarray[numpy.float64, _Shape[1, 1]], dt: seconds) -> numpy.ndarray[numpy.float64, _Shape[2, 1]]: 
        """
        Updates the state estimate of the arm.

        :param currentXhat: The current state estimate.

        :param u: The system inputs (voltage).

        :param dt: The time difference between controller updates.
        """
    @staticmethod
    def estimateMOI(length: meters, mass: kilograms) -> kilogram_square_meters: 
        """
        Calculates a rough estimate of the moment of inertia of an arm given its
        length and mass.

        :param length: The length of the arm.

        :param mass: The mass of the arm.

        :returns: The calculated moment of inertia.
        """
    def getAngle(self) -> radians: 
        """
        Returns the current arm angle.

        :returns: The current arm angle.
        """
    def getCurrentDraw(self) -> amperes: 
        """
        Returns the arm current draw.

        :returns: The arm current draw.
        """
    def getVelocity(self) -> radians_per_second: 
        """
        Returns the current arm velocity.

        :returns: The current arm velocity.
        """
    def hasHitLowerLimit(self, x: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> bool: 
        """
        Returns whether the arm has hit the lower limit.

        :param x: The current arm state.

        :returns: Whether the arm has hit the lower limit.
        """
    def hasHitUpperLimit(self, x: numpy.ndarray[numpy.float64, _Shape[2, 1]]) -> bool: 
        """
        Returns whether the arm has hit the upper limit.

        :param x: The current arm state.

        :returns: Whether the arm has hit the upper limit.
        """
    def setInputVoltage(self, voltage: volts) -> None: 
        """
        Sets the input voltage for the elevator.

        :param voltage: The input voltage.
        """
    pass
class XboxControllerSim(GenericHIDSim):
    """
    Class to control a simulated Xbox 360 or Xbox One controller.
    """
    @typing.overload
    def __init__(self, joystick: wpilib._wpilib.XboxController) -> None: 
        """
        Constructs from a XboxController object.

        :param joystick: controller to simulate

        Constructs from a joystick port number.

        :param port: port number
        """
    @typing.overload
    def __init__(self, port: int) -> None: ...
    def setAButton(self, state: bool) -> None: ...
    def setBButton(self, state: bool) -> None: ...
    def setBackButton(self, state: bool) -> None: ...
    def setBumper(self, hand: wpilib.interfaces._interfaces.GenericHID.Hand, state: bool) -> None: ...
    def setStartButton(self, state: bool) -> None: ...
    def setStickButton(self, hand: wpilib.interfaces._interfaces.GenericHID.Hand, state: bool) -> None: ...
    def setTriggerAxis(self, hand: wpilib.interfaces._interfaces.GenericHID.Hand, value: float) -> None: ...
    def setX(self, hand: wpilib.interfaces._interfaces.GenericHID.Hand, value: float) -> None: ...
    def setXButton(self, state: bool) -> None: ...
    def setY(self, hand: wpilib.interfaces._interfaces.GenericHID.Hand, value: float) -> None: ...
    def setYButton(self, state: bool) -> None: ...
    pass
def getProgramStarted() -> bool:
    pass
def isTimingPaused() -> bool:
    pass
def pauseTiming() -> None:
    pass
def restartTiming() -> None:
    pass
def resumeTiming() -> None:
    pass
def setProgramStarted() -> None:
    pass
def setRuntimeType(type: hal._wpiHal.RuntimeType) -> None:
    pass
def stepTiming(delta: seconds) -> None:
    pass
def stepTimingAsync(delta: seconds) -> None:
    pass
def waitForProgramStart() -> None:
    pass
